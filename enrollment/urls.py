from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet, EnrollmentViewSet, verify_payment


router = DefaultRouter()
router.register(r'transactions', TransactionViewSet)
router.register(r'enrollments', EnrollmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('verify-payment/', verify_payment, name='verify_payment'),
]