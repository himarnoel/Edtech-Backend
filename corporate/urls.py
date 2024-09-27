from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CorporateInquiryViewSet

router = DefaultRouter()
router.register(r'coporate_inquiry', CorporateInquiryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
