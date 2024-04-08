from django.urls import path
from .views import UserSignUpAPIView,UserLoginAPIView

urlpatterns = [
    path("signup", UserSignUpAPIView.as_view()),
    path("login", UserLoginAPIView.as_view()),
]
