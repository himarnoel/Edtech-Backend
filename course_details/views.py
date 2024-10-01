from django.shortcuts import render
from rest_framework import viewsets
from .models import Module, Lesson,CourseProgress
from .serializer import ModuleSerializer, LessonSerializer, CourseContentSerializer,UserProgressSerializer
from rest_framework.decorators import action
from core.utils import success_message, error_message
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import viewsets
from .models import Course
from rest_framework.permissions import IsAuthenticated
from enrollment.models import Enrollment
from rest_framework import viewsets


# Create your views here.


class BaseCRUDViewSet(viewsets.ModelViewSet):
    """
    Base class for handling POST, PUT, and PATCH,DELETE and GET both single and all requests in one Class.
    """

    def handle_create_update(self, request, *args, **kwargs):
        """
        Handles creation (POST), update (PUT), and partial update (PATCH) requests.
        """
        # Determine if the request is a POST or an update request
        is_post = request.method == 'POST'
        try:
            if is_post:
                # For POST requests, there is no instance to update
                instance = None
                data = request.data
            else:
                # For PUT and PATCH requests, get the existing instance
                instance = self.get_object()
                data = request.data

            # Create a serializer instance with the data and instance
            serializer = self.get_serializer(
                instance, data=data, partial=not is_post)

            # Check if the data is valid
            if serializer.is_valid():
                # Save the instance if valid data is provided
                obj = serializer.save()
                status_code = status.HTTP_201_CREATED if is_post else status.HTTP_200_OK
                # Return a success response with the serializer data
                payload = success_message(
                    message="Created Successfully" if is_post else "Updated Successfully",
                    data=serializer.data
                )
                return Response(data=payload, status=status_code)

            # Handle validation errors
            first_key = next(iter(serializer.errors))
            error_msg = serializer.errors[first_key][0]
            payload = error_message(
                message=error_msg if error_msg else f"{first_key.title()} is empty"
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

        except NotFound:
            # Handle case where object is not found
            payload = error_message(message="ID not found.")
            return Response(data=payload, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            payload = error_message(message="An error occurred")
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        # Attempt to retrieve the object to be deleted
        try:
            instance = self.get_object()
            # Perform the delete operation
            self.perform_destroy(instance)
            payload = success_message(
                message="Deleted successfully", data="")
            # Return a success response with a 204 status code
            return Response(data=payload, status=status.HTTP_204_NO_CONTENT)

        except NotFound:
            payload = error_message(
                message="Id not found")
            return Response(data=payload, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Handle any unexpected exceptions that may occur
            payload = error_message(
                message="An error occurred during deletion")
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of objects from the queryset.
        """

        queryset = self.filter_queryset(self.get_queryset())

        # Paginate the queryset if required
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # If no pagination is required, serialize and return the full queryset
        serializer = self.get_serializer(queryset, many=True)
        payload = success_message(
            message="Fetched successfully", data=serializer.data)
        return Response(data=payload, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            payload = success_message(
                message="Fetched successfully", data=serializer.data)
            return Response(data=payload, status=status.HTTP_200_OK)
        except NotFound:
            payload = error_message(message="ID not found")
            return Response(data=payload, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            payload = error_message(
                message="An error occurred during retrieval.")
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)


class ModuleViewSet(BaseCRUDViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    # You can call handle_create_update for create, update, and partial_update methods.
    def create(self, request, *args, **kwargs):
        return self.handle_create_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return self.handle_create_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self.handle_create_update(request, *args, **kwargs)


class LessonViewSet(BaseCRUDViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    # You can call handle_create_update for create, update, and partial_update methods.
    def create(self, request, *args, **kwargs):
        return self.handle_create_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return self.handle_create_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self.handle_create_update(request, *args, **kwargs)



class UserProgressViewSet(viewsets.ModelViewSet):
    queryset = CourseProgress.objects.all()
    serializer_class = UserProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter the queryset to show only the progress for the logged-in user
        user = self.request.user
        return CourseProgress.objects.filter(user=user) 

    @action(detail=False, methods=['post'])
    def complete_lesson(self, request):
        # Retrieve user and lesson_id from the request data
        user = request.user
        lesson_id = request.data.get('lesson_id')
        course_id = request.data.get('course_id')

        if not lesson_id or not course_id:
            return Response({'error': 'Lesson ID and Course ID are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the Lesson object
        try:
            lesson = Lesson.objects.get(id=lesson_id)
        except Lesson.DoesNotExist:
            return Response({'error': 'Lesson not found'}, status=status.HTTP_404_NOT_FOUND)

        # Fetch the Course object
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the progress already exists for the user and course
        progress, created =CourseProgress.objects.get_or_create(user=user, course=course)

        # Mark the lesson as completed
        lesson.completed = True
        lesson.save()

        # Add the lesson to the user's completed lessons if not already there
        progress.completed_lessons.add(lesson)
        progress.save()

        return Response({'status': 'Lesson completed successfully', 'progress_id': progress.id})




class CourseContentViewset(BaseCRUDViewSet):
    """
    ViewSet for handling CRUD operations on Courses.
    Inherits from BaseCRUDViewSet.
    """
    queryset = Course.objects.all()
    serializer_class = CourseContentSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        """
        Handle GET request to retrieve a single course and check if the user has paid for it.
        """
        try:
            # Retrieve the course instance
            instance = self.get_object()

            # Check if the user has paid for the course
            is_paid = Enrollment.objects.filter(
                user=request.user, course=instance, transaction__status='success'
            ).exists()

            # Serialize the course content
            serializer = self.get_serializer(instance)

            # Prepare the response data
            data = {

                "isPaid": is_paid,
                "data": serializer.data,

            }
            payload = success_message(
                message="Fetched successfully", data=data)
            return Response(data=payload, status=status.HTTP_200_OK)

        except Course.DoesNotExist:
            payload = error_message(
                message="Course not found")
            return Response(data=payload, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print(f"e {e}")
            payload = error_message(
                message="Error coccured during retrival")
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
