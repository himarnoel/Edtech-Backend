from django.shortcuts import render
from rest_framework import viewsets
from .models import Category,  Course,CourseReview
from .serializer import CategorySerializer,  CourseSerializer, CourseReviewSerializer
from .utils import success_message, error_message
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.http import Http404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny,BasePermission
from .baseviewclass import BaseCRUDViewSet

# Create your views here.
class CategoryViewSet(BaseCRUDViewSet):
    queryset = Category.objects.order_by('name')
    serializer_class = CategorySerializer
    

    # You can call handle_create_update for create, update, and partial_update methods.
    def create(self, request, *args, **kwargs):
        return self.handle_create_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return self.handle_create_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self.handle_create_update(request, *args, **kwargs)



class CourseViewSet(BaseCRUDViewSet):
    queryset = Course.objects.order_by('title')
    serializer_class = CourseSerializer

    def create(self, request, *args, **kwargs):
        return self.handle_create_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return self.handle_create_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self.handle_create_update(request, *args, **kwargs)


class IsEmailVerified(BasePermission):
    def has_permission(self, request, view):
        return request.user.email_verified

class CourseReviewViewSet(BaseCRUDViewSet):
    queryset = CourseReview.objects.all()
    serializer_class = CourseReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Automatically set the user field to the current user during creation.
        """
    
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """
        Ensure that the user field is set to the current user during updates.
        """
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a new review ensuring the course is valid and the user is authenticated.
        """
        course_id = request.data.get('course')
        if not Course.objects.filter(course_id=course_id).exists():
            payload = error_message(message="Invalid course ID")
            return Response(data=payload, status=status.HTTP_404_NOT_FOUND)
        
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Update an existing review ensuring the course is valid.
        """
        course_id = request.data.get('course')
        if not Course.objects.filter(id=course_id).exists():
           payload = error_message(message="Invalid course ID")
           return Response(data=payload, status=status.HTTP_404_NOT_FOUND)
        
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Partially update an existing review ensuring the course is valid.
        """
        course_id = request.data.get('course')
        if not Course.objects.filter(id=course_id).exists():
           payload = error_message(message="Invalid course ID")
           return Response(data=payload, status=status.HTTP_404_NOT_FOUND)
        
        return super().partial_update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of all CourseReview objects without pagination.
        """
        # print(request.headers.get('Authorization'))
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        payload = success_message(
            message="Fetched successfully", data=serializer.data
        )
        return Response(data=payload, status=status.HTTP_200_OK) 