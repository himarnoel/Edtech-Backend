from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EnrollmentViewSet,TransactionViewSet

# Create a router and register your viewsets
router = DefaultRouter()
router.register(r'payment', TransactionViewSet, basename='transaction')
router.register(r'', EnrollmentViewSet, basename='enrollment')


urlpatterns = router.urls