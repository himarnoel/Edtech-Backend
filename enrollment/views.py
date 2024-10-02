from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Transaction, Enrollment
from courses.models import Course
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

def error_response(message, status_code=status.HTTP_400_BAD_REQUEST):
    payload = error_message(message=message)
    return Response(data=payload, status=status_code)

def initialize_payment(user, amount):
    headers = {
        "Authorization": f"Bearer {os.getenv('PAYSTACK_SECRET_KEY')}",
        "Content-Type": "application/json",
    }
    payload = {
        "email": user.email,
        "amount": int(amount * 100),  # Paystack expects amount in kobo (100 kobo = 1 Naira)
        "reference": str(uuid.uuid4()),
        "callback_url": f"{os.getenv('FE_LINK')}/dashboard/payment-confirmation",
    }
    response = requests.post(
        "https://api.paystack.co/transaction/initialize",
        headers=headers,
        json=payload,
    )
    return response

class BaseCRUDViewSet(viewsets.ModelViewSet):
    def handle_create_update(self, request, *args, **kwargs):
        is_post = request.method == "POST"
        try:
            instance = None if is_post else self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=not is_post)

            if serializer.is_valid():
                obj = serializer.save()
                status_code = status.HTTP_201_CREATED if is_post else status.HTTP_200_OK
                message = "Created Successfully" if is_post else "Updated Successfully"
                payload = success_message(message=message, data=serializer.data)
                return Response(data=payload, status=status_code)

            error_msg = next(iter(serializer.errors.values()))[0]
            return error_response(error_msg)

        except Exception:
            return error_response("An error occurred")

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            payload = success_message(message="Deleted successfully", data={})
            return Response(data=payload, status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return error_response("An error occurred during deletion")

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
        except Exception:
            return error_response("An error occurred during retrieval.")

class TransactionViewSet(BaseCRUDViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        course_ids = request.data.get("courses", [])  # List of course IDs
        amount = request.data.get("amount")
        print("course_ids", course_ids)

        # Validate the amount
        try:
            amount = float(amount)
            if amount <= 0:
                return error_response("Amount must be greater than zero")
        except (ValueError, TypeError):
            return error_response("Invalid amount provided")

        # Check if the user has already paid for any of the courses
        existing_courses = set(Transaction.objects.filter(
        user=user).values_list('courses__course_id', flat=True))  # Change 'id' to 'course_id'

        if existing_courses.intersection(course_ids):
            return error_response(f"User already paid for course(s): {list(existing_courses.intersection(course_ids))}")

        response = initialize_payment(user, amount)
        response_data = response.json()

        if response_data["status"]:
            # Create a transaction and link to courses
            transaction = Transaction.objects.create(
                user=user,
                amount=amount,
                reference=response_data["data"]["reference"],
                status="Pending",
            )
            transaction.courses.set(course_ids)

            payload = success_message(
                message="Payment initialized successfully",
                data={"payment_url": response_data["data"]["authorization_url"]},
            )
            return Response(data=payload, status=status.HTTP_200_OK)
        else:
            return error_response("Payment initialization failed")


class EnrollmentViewSet(BaseCRUDViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = Enrollment.objects.filter(user=user)  # Filter enrollments by the authenticated user
        serializer = self.get_serializer(queryset, many=True)
        payload = success_message(message="Courses fetched successfully", data=serializer.data)
        return Response(data=payload, status=status.HTTP_200_OK) 

    def create(self, request, *args, **kwargs):
        user = request.user
        course_ids = request.data.get("courses", [])  # List of course IDs

        if not course_ids:
            return error_response("No courses provided")

        # Check if the user is already enrolled in any of the courses
        existing_enrollments = Enrollment.objects.filter(user=user, course__in=course_ids).values_list('course', flat=True)
        if existing_enrollments:
            return error_response(f"User already enrolled in course(s): {existing_enrollments}")

        # Ensure payment is successful for all courses
        successful_transactions = Transaction.objects.filter(user=user, course__in=course_ids, status="success")
        if successful_transactions.count() != len(course_ids):
            return error_response("Payment not completed for all courses")

        # Enroll the user in each course
        enrollments = []
        for transaction in successful_transactions:
            enrollment = Enrollment.objects.create(user=user, course=transaction.course, transaction=transaction, isPaid=True)
            enrollments.append(enrollment)

        serializer = self.get_serializer(enrollments, many=True)
        payload = success_message(message="Enrolled Successfully", data=serializer.data)
        return Response(data=payload, status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(["GET"])
def verify_payment(request):
    reference = request.GET.get("reference")
    if not reference:
        return error_response("Reference is required", status_code=status.HTTP_400_BAD_REQUEST)

    headers = {
        "Authorization": f"Bearer {os.getenv('PAYSTACK_SECRET_KEY')}",
        "Content-Type": "application/json",
    }
    response = requests.get(f"https://api.paystack.co/transaction/verify/{reference}", headers=headers)

    if response.status_code != 200:
        return error_response("Error retrieving payment status from Paystack", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        response_data = response.json()
    except ValueError:
        return error_response("Invalid response from Paystack", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if response_data["status"]:
        try:
            # Find the transaction by reference
            transactions = Transaction.objects.filter(reference=reference)
            if not transactions.exists():
                return error_response("Transaction not found", status_code=status.HTTP_404_NOT_FOUND)

            # Update the transaction status
            for transaction in transactions:
                transaction.status = response_data["data"]["status"]
                transaction.save()

                # If payment was successful, enroll the user in the associated courses
                if transaction.status.lower() == "success":
                    for course in transaction.courses.all():
                        # Check if the user is already enrolled
                        if not Enrollment.objects.filter(user=transaction.user, course=course).exists():
                            Enrollment.objects.create(
                                user=transaction.user,
                                course=course,
                                transaction=transaction,
                                isPaid=True
                            )

            payload = success_message(message="Enrolled Successfully", data="")
            return Response(data=payload, status=status.HTTP_201_CREATED)     
        except Transaction.DoesNotExist:
            return error_response("Transaction not found", status_code=status.HTTP_404_NOT_FOUND)
    else:
        return error_response(response_data.get("message", "Payment verification failed"))
