from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ModuleViewSet, LessonViewSet

# Create a router and register your viewsets with it
router = DefaultRouter()
router.register(r'modules', ModuleViewSet, basename='modules')
router.register(r'lessons', LessonViewSet, basename='lessons')

# The API URLs are now determined automatically by the router
urlpatterns = router.urls
