from django.urls import path
from .views import UserSignUpAPIView, UserLoginAPIView, EmailVerificationAPIView, PasswordResetRequestAPIView, PasswordResetAPIView

urlpatterns = [
    path("signup", UserSignUpAPIView.as_view()),
    path('verify-email/<str:token>/',
         EmailVerificationAPIView.as_view(), name='verify_email'),
    #  path('google-login/', GoogleLoginView.as_view(), name='google_login'),
    path("login", UserLoginAPIView.as_view()),
    path('reset-password/request/', PasswordResetRequestAPIView.as_view(),
         name='password_reset_request'),
    path('reset-password/<str:uidb64>/<str:token>/',
         PasswordResetAPIView.as_view(), name='password_reset'),
]
