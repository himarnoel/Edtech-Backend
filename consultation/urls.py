from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConsultationView


urlpatterns = [
    path('consult/', ConsultationView.as_view(), name="consultation"),
]
