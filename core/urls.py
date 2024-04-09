from django.urls import path
from .views import UserSignUpAPIView,UserLoginAPIView, EmailVerificationAPIView

urlpatterns = [
    path("signup", UserSignUpAPIView.as_view()),
    path('verify-email/<str:token>/', EmailVerificationAPIView.as_view(), name='verify_email'),
    path("login", UserLoginAPIView.as_view()),
]
