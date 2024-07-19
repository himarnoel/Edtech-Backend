from django.shortcuts import render
from rest_framework import viewsets
from .models import Category, Subcategory, Course
from .serializer import CategorySerializer, SubcategorySerializer, CourseSerializer
from .utils import success_message, error_message
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.http import Http404
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions

# Create your views here.


class BaseCRUDViewSet(viewsets.ModelViewSet):
    # permission_classes=[permissions.IsAuthenticated]
    """
    Base class for handling POST, PUT, and PATCH,DELETE and GET both single and all requests in one Class.
    """

    def handle_create_update(self, request, *args, **kwargs):
        """
        Handles creation (POST), update (PUT), and partial update (PATCH) requests.
        """
        # Determine if the request is a POST or an update request
        is_post = request.method == "POST"
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
            serializer = self.get_serializer(instance, data=data, partial=not is_post)

            # Check if the data is valid
            if serializer.is_valid():
                # Save the instance if valid data is provided
                obj = serializer.save()
                status_code = status.HTTP_201_CREATED if is_post else status.HTTP_200_OK
                # Return a success response with the serializer data
                payload = success_message(
                    message=(
                        "Created Successfully" if is_post else "Updated Successfully"
                    ),
                    data=serializer.data,
                )
                return Response(data=payload, status=status_code)

            # Handle validation errors
            first_key = next(iter(serializer.errors))
            error_msg = serializer.errors[first_key][0]
            payload = error_message(
                message=f"{first_key.title()} is empty" if error_msg else error_msg
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
            payload = success_message(message="Deleted successfully", data="")
            # Return a success response with a 204 status code
            return Response(data=payload, status=status.HTTP_204_NO_CONTENT)

        except NotFound:
            payload = error_message(message="Id not found")
            return Response(data=payload, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Handle any unexpected exceptions that may occur
            payload = error_message(message="An error occurred during deletion")
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

    def get_paginated_response(self, data):
        """
        Pagination
        """
        paginator = self.paginator
        if paginator is None:
            paginator = PageNumberPagination()
        page = paginator.page
        pagination_metadata = {
            "pageNumber": page.number,
            "pageSize": paginator.page_size,
            "totalPages": paginator.page.paginator.num_pages,
            "totalRecords": paginator.page.paginator.count,
        }

        # Create paginated response payload
        payload = success_message(
            message="Fetched successfully",
            data={"pageMeta": pagination_metadata, "results": data},
        )
        return Response(data=payload, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of objects from the queryset.
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)
            payload = success_message(
                message="Fetched successfully", data=serializer.data
            )
            return Response(data=payload, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            payload = success_message(
                message="Fetched successfully", data=serializer.data
            )
            return Response(data=payload, status=status.HTTP_200_OK)
        except NotFound:
            payload = error_message(message="ID not found")
            return Response(data=payload, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            payload = error_message(message="An error occurred during retrieval.")
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(BaseCRUDViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    

    # You can call handle_create_update for create, update, and partial_update methods.
    def create(self, request, *args, **kwargs):
        return self.handle_create_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return self.handle_create_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self.handle_create_update(request, *args, **kwargs)


class SubcategoryViewSet(BaseCRUDViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer

    def create(self, request, *args, **kwargs):
        return self.handle_create_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return self.handle_create_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self.handle_create_update(request, *args, **kwargs)


class CourseViewSet(BaseCRUDViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
   

    def create(self, request, *args, **kwargs):
        return self.handle_create_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return self.handle_create_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self.handle_create_update(request, *args, **kwargs)
