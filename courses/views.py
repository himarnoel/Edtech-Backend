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
from rest_framework import permissions
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




class CourseReviewViewSet(BaseCRUDViewSet):
    queryset = CourseReview.objects.all()
    serializer_class = CourseReviewSerializer

    def create(self, request, *args, **kwargs):
        return self.handle_create_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return self.handle_create_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self.handle_create_update(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of all CourseReview objects without pagination.
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        payload = success_message(
            message="Fetched successfully", data=serializer.data
        )
        return Response(data=payload, status=status.HTTP_200_OK)