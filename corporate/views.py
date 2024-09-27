from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import CorporateInquiryModel
from .serializers import CorporateInquirySerializer


class CorporateInquiryViewSet(viewsets.ModelViewSet):
    queryset = CorporateInquiryModel.objects.all()
    serializer_class = CorporateInquirySerializer

    # Custom CREATE response
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({
                'status': 'success',
                'message': 'Blog post updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'status': 'Error',
            'message': 'Error Creating instance',
        }, status=status.HTTP_400_BAD_REQUEST)

    # Custom UPDATE response
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({
                'status': 'success',
                'message': 'Blog post updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'status': 'Error',
            'message': 'Error updating instance',
        }, status=status.HTTP_400_BAD_REQUEST)

    # Custom DELETE response
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        # Custom response format for successful deletion
        return Response({
            'status': 'success',
            'message': 'Blog post deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)

    # Custom RETRIEVE response
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # Custom response format for retrieving a single blog post
        return Response({
            'status': 'success',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    # Custom LIST response
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        # Custom response format for listing all blog posts
        return Response({
            'status': 'success',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
