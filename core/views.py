from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import UserSignUpSerializer, UserLoginSerializer, PasswordResetRequestSerializer, PasswordResetSerializer
from .utils import send_verification_email, send_resetPassword_email
from django.contrib.auth.tokens import default_token_generator
import uuid
from django.utils.http import urlsafe_base64_decode
from rest_api_payload import success_response, error_response
from .utils import error_message, success_message


class UserSignUpAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # serializer.is_valid(raise_exception=True)
            user = serializer.save()
            verification_token = str(user.verification_token)
            send_verification_email(user.email, verification_token)
            payload = success_message(
                message="Signup Successfully", data=serializer.data)
            return Response(data=payload, status=status.HTTP_201_CREATED)
        firstkey = next(iter(serializer.errors))
        payload = error_message(message=serializer.errors[firstkey][0])
        return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationAPIView(generics.GenericAPIView):
    def get(self, request, token):
        try:
            # Try to convert the token to a UUID
            uuid_obj = uuid.UUID(token)
        except ValueError:

            payload = error_message(message="Invalid token")
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = CustomUser.objects.get(verification_token=token)
            if user.email_verified:
                payload = error_message(message="Email already verified")
                return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
            else:
                user.email_verified = True
                user.save()
                payload = success_message(
                    message="Email verified successfully.", data="Nil")
                return Response(data=payload, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            payload = error_message(message="Invalid token")
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                payload = error_message(message="User does not exist")
                return Response(data=payload, status=status.HTTP_401_UNAUTHORIZED)

            if not user.email_verified:
                payload = error_message(message="Email not verified")
                return Response(data=payload, status=status.HTTP_401_UNAUTHORIZED)

            if not user.check_password(password):
                payload = error_message(message="Wrong Password")
                return Response(data=payload, status=status.HTTP_401_UNAUTHORIZED)

            refresh = RefreshToken.for_user(user)
            payload = success_message(message="Login Successful", data={
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
            return Response(data=payload, status=status.HTTP_200_OK)
        firstkey = next(iter(serializer.errors))
        payload = error_message(message=serializer.errors[firstkey][0])
        return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestAPIView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                payload = error_message(message="User not found")
                return Response(data=payload, status=status.HTTP_404_NOT_FOUND)

            # Generate reset token
            token = default_token_generator.make_token(user)
            send_resetPassword_email(user, token)
            payload = success_message(
                message="Password reset link sent", data=serializer.data)
            return Response(data=payload, status=status.HTTP_200_OK)

        firstkey = next(iter(serializer.errors))
        payload = error_message(message=serializer.errors[firstkey][0])
        return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetAPIView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None
            payload = error_message(message="User not found")
            return Response(data=payload, status=status.HTTP_404_NOT_FOUND)

        if user is not None and default_token_generator.check_token(user, token):
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.is_valid(raise_exception=True)
                new_password = serializer.validated_data['new_password']
                user.set_password(new_password)
                user.save()
                payload = success_message(
                    message="Password reset successful", data="")
                return Response(data=payload, status=status.HTTP_200_OK)
            firstkey = next(iter(serializer.errors))
            payload = error_message(message=serializer.errors[firstkey][0])
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

        else:
            payload = error_message(message="Invalid reset link")
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
