from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import UserSignUpSerializer, UserLoginSerializer
from .utils import  send_verification_email
import uuid


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