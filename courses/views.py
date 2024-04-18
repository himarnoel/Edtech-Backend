from django.shortcuts import render
from rest_framework import viewsets
from .models import Category, Subcategory, Course
from .serializer import CategorySerializer, SubcategorySerializer, CourseSerializer
from .utils import success_message, error_message
from rest_framework import generics, status
from rest_framework.response import Response

# Create your views here.


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            obj = serializer.save()

            payload = success_message(
                message="Created Category Successfully", data=serializer.data)
            return Response(data=payload, status=status.HTTP_201_CREATED)

        # Custom Validation error hadling
        first_key = next(iter(serializer.errors))
        error_msg = serializer.errors[first_key][0]
        payload = error_message(message= f"{first_key.title()} is empty" if error_msg else error_message)
        return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)


class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            obj = serializer.save()

            payload = success_message(
                message="Created Successfully", data=serializer.data)
            return Response(data=payload, status=status.HTTP_201_CREATED)

        # Custom Validation error hadling
        first_key = next(iter(serializer.errors))
        error_msg = serializer.errors[first_key][0]
        payload = error_message(message= f"{first_key.title()} is empty" if error_msg else error_message)
        return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            obj = serializer.save()

            payload = success_message(
                message="Created Successfully", data=serializer.data)
            return Response(data=payload, status=status.HTTP_201_CREATED)

        # Custom Validation error hadling
        first_key = next(iter(serializer.errors))
        error_msg = serializer.errors[first_key][0]
        payload = error_message(message= f"{first_key.title()} is empty" if error_msg else error_message)
        return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
