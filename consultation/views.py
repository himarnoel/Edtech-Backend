from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from .models import ConsultationModel
from .serializers import ConsultationSerializer
from course_details.views import BaseCRUDViewSet
from rest_api_payload import success_response, error_response
from django.contrib.auth import get_user_model
from .serializers import ConsultationSerializer
from .utils import send_consult_email_admin, send_consult_email_user


class ConsultationView(generics.ListCreateAPIView):
    queryset = ConsultationModel.objects.all()
    serializer_class = ConsultationSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        payload = success_response(
            status="Success",
            message="Consultations fetched successfully",
            data=serializer.data
        )
        return Response(payload, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)

            consultation_data = serializer.validated_data
            print(f"consultation_data {consultation_data['phone_number']}")

            send_consult_email_user(
                name=consultation_data['name'],
                email=consultation_data['email'],
            )

            send_consult_email_admin(
                name=consultation_data['name'],
                email=consultation_data['email'],
                phone_number=consultation_data['phone_number']
            )
            payload = success_response(
                status="Success",
                message="Consultation created successfully",
                data=serializer.data
            )
            return Response(payload, status=status.HTTP_201_CREATED)

        payload = error_response(
            status="Error",
            message="Failed to create consultation",
        )
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)
