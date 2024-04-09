from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import UserSignUpSerializer, UserLoginSerializer, PasswordResetRequestSerializer, PasswordResetSerializer
from .utils import  send_verification_email, send_resetPassword_email
from django.contrib.auth.tokens import default_token_generator
import uuid
from django.utils.http import urlsafe_base64_decode




class UserSignUpAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSignUpSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        verification_token = str(user.verification_token)
        send_verification_email(user.email, verification_token)
        return Response({"message": "User created successfully. Verification email sent."}, status=status.HTTP_201_CREATED)



class EmailVerificationAPIView(generics.GenericAPIView):
    def get(self, request, token):
        try:
            # Try to convert the token to a UUID
            uuid_obj = uuid.UUID(token)
        except ValueError:
            # If the token is not a valid UUID, return an error response
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        try:
         user = CustomUser.objects.get(verification_token=token)
         if user.email_verified:
            return Response({"message": "Email already verified"}, status=status.HTTP_200_OK)
         else:
            user.email_verified = True
            user.save()
            return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(generics.CreateAPIView):
   serializer_class = UserLoginSerializer
   def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.email_verified:
            return Response({"error": "Email not verified"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class PasswordResetRequestAPIView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            user =  CustomUser.objects.get(email=email)
        except user.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Generate reset token
        token = default_token_generator.make_token(user)
        send_resetPassword_email(user, token)
        return Response({"detail": "Password reset link sent"}, status=status.HTTP_200_OK)
    

class PasswordResetAPIView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()
            return Response({"detail": "Password reset successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid reset link"}, status=status.HTTP_400_BAD_REQUEST)