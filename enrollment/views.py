# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Transaction, Enrollment
from .serializers import TransactionSerializer, EnrollmentSerializer
import uuid
import requests
from courses.utils import success_message, error_message
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated


class BaseCRUDViewSet(viewsets.ModelViewSet):
    """
    Base class for handling POST, PUT, PATCH, DELETE, and GET requests in one Class.
    """

    def handle_create_update(self, request, *args, **kwargs):
        """
        Handles creation (POST), update (PUT), and partial update (PATCH) requests.
        """
        # Determine if the request is a POST or an update request
        is_post = request.method == "POST"
        try:
            if is_post:
                # For POST requests, there is no instance to update
                instance = None
                data = request.data
            else:
                # For PUT and PATCH requests, get the existing instance
                instance = self.get_object()
                data = request.data

            # Create a serializer instance with the data and instance
            serializer = self.get_serializer(instance, data=data, partial=not is_post)

            # Check if the data is valid
            if serializer.is_valid():
                # Save the instance if valid data is provided
                obj = serializer.save()
                status_code = status.HTTP_201_CREATED if is_post else status.HTTP_200_OK
                # Return a success response with the serializer data
                payload = success_message(
                    message=(
                        "Created Successfully" if is_post else "Updated Successfully"
                    ),
                    data=serializer.data,
                )
                return Response(data=payload, status=status_code)

            # Handle validation errors
            first_key = next(iter(serializer.errors))
            error_msg = serializer.errors[first_key][0]
            payload = error_message(
                message=f"{first_key.title()} is empty" if error_msg else error_msg
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

        except NotFound:
            # Handle case where object is not found
            payload = error_message(message="ID not found.")
            return Response(data=payload, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            payload = error_message(message="An error occurred")
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        # Attempt to retrieve the object to be deleted
        try:
            instance = self.get_object()
            # Perform the delete operation
            self.perform_destroy(instance)
            payload = success_message(message="Deleted successfully", data="")
            # Return a success response with a 204 status code
            return Response(data=payload, status=status.HTTP_204_NO_CONTENT)

        except NotFound:
            payload = error_message(message="Id not found")
            return Response(data=payload, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Handle any unexpected exceptions that may occur
            payload = error_message(message="An error occurred during deletion")
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of objects from the queryset.
        """

        queryset = self.filter_queryset(self.get_queryset())

        # Paginate the queryset if required
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # If no pagination is required, serialize and return the full queryset
        serializer = self.get_serializer(queryset, many=True)
        payload = success_message(message="Fetched successfully", data=serializer.data)
        return Response(data=payload, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            payload = success_message(
                message="Fetched successfully", data=serializer.data
            )
            return Response(data=payload, status=status.HTTP_200_OK)
        except NotFound:
            payload = error_message(message="ID not found")
            return Response(data=payload, status=status.HTTP_404_NOT_FOUND)
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

        # Make payment through Paystack API
        # You need to replace 'PAYSTACK_SECRET_KEY' with your actual Paystack secret key
        headers = {
            "Authorization": "Bearer PAYSTACK_SECRET_KEY",
            "Content-Type": "application/json",
        }
        payload = {
            "email": user.email,
            "amount": amount,
            "reference": str(uuid.uuid4()),  # Generate a unique reference
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
            return Response(
                data=payload,
                status=status.HTTP_400_BAD_REQUEST,
            )


class EnrollmentViewSet(BaseCRUDViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
