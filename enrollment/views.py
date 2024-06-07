from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Transaction, Enrollment
from .serializers import TransactionSerializer, EnrollmentSerializer
import uuid
import requests
from courses.utils import success_message, error_message
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class BaseCRUDViewSet(viewsets.ModelViewSet):
    def handle_create_update(self, request, *args, **kwargs):
        is_post = request.method == "POST"
        try:
            if is_post:
                instance = None
                data = request.data
            else:
                instance = self.get_object()
                data = request.data

            serializer = self.get_serializer(instance, data=data, partial=not is_post)

            if serializer.is_valid():
                obj = serializer.save()
                status_code = status.HTTP_201_CREATED if is_post else status.HTTP_200_OK
                payload = success_message(
                    message="Created Successfully" if is_post else "Updated Successfully",
                    data=serializer.data,
                )
                return Response(data=payload, status=status_code)

            first_key = next(iter(serializer.errors))
            error_msg = serializer.errors[first_key][0]
            payload = error_message(
                message=f"{first_key.title()} is empty" if error_msg else error_msg
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            payload = error_message(message="An error occurred")
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            payload = success_message(message="Deleted successfully", data="")
            return Response(data=payload, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            payload = error_message(message="An error occurred during deletion")
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        payload = success_message(message="Fetched successfully", data=serializer.data)
        return Response(data=payload, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            payload = success_message(message="Fetched successfully", data=serializer.data)
            return Response(data=payload, status=status.HTTP_200_OK)
        except Exception as e:
            payload = error_message(message="An error occurred during retrieval.")
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

class TransactionViewSet(BaseCRUDViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course")
        amount = request.data.get("amount")

        headers = {
            "Authorization": f"Bearer {os.getenv('PAYSTACK_SECRET_KEY')}",
            "Content-Type": "application/json",
        }
        payload = {
            "email": user.email,
            "amount": amount,
            "reference": str(uuid.uuid4()),
            "callback_url": "http://localhost:8000/enrollment/api/verify-payment/",
        }
        response = requests.post(
            "https://api.paystack.co/transaction/initialize",
            headers=headers,
            json=payload,
        )
        response_data = response.json()

        if response_data["status"]:
            transaction = Transaction.objects.create(
                user=user,
                course_id=course_id,
                amount=amount,
                reference=response_data["data"]["reference"],
                status="Pending",
            )
            payload = success_message(
                message="Created Successfully",
                data={"payment_url": response_data["data"]["authorization_url"]},
            )
            return Response(data=payload, status=status.HTTP_200_OK)
        else:
            payload = error_message(message="Payment initialization failed")
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

class EnrollmentViewSet(BaseCRUDViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course")

        # Check if the user is already enrolled in the course
        if Enrollment.objects.filter(user=user, course_id=course_id).exists():
            payload = error_message(message="User already enrolled in this course")
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

        # Check if the payment was successful
        try:
            transaction = Transaction.objects.get(user=user, course_id=course_id, status="completed")
        except Transaction.DoesNotExist:
            payload = error_message(message="Payment not completed")
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

        # Create the enrollment if payment is confirmed
        enrollment = Enrollment.objects.create(user=user, course_id=course_id, transaction=transaction)
        serializer = self.get_serializer(enrollment)
        payload = success_message(message="Enrolled Successfully", data=serializer.data)
        return Response(data=payload, status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(["GET"])
def verify_payment(request):
    reference = request.GET.get("reference")
    if not reference:
        return Response({"detail": "Reference is required"}, status=status.HTTP_400_BAD_REQUEST)

    headers = {
        "Authorization": f"Bearer {os.getenv('PAYSTACK_SECRET_KEY')}",
        "Content-Type": "application/json",
    }
    response = requests.get(f"https://api.paystack.co/transaction/verify/{reference}", headers=headers)

    if not response.content:
        return Response({"detail": "No response from Paystack"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        response_data = response.json()
    except ValueError:
        return Response({"detail": "Invalid response from Paystack"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if response_data["status"]:
        try:
            transaction = Transaction.objects.get(reference=reference)
            transaction.status = response_data["data"]["status"]
            transaction.save()
            return Response({"detail": "Payment verified successfully"})
        except Transaction.DoesNotExist:
            return Response({"detail": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"detail": response_data.get("message", "Payment verification failed")}, status=status.HTTP_400_BAD_REQUEST)
