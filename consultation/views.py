from rest_framework import viewsets
from .models import ConsultationModel
from .serializers import ConsultationSerializer
from course_details.views import BaseCRUDViewSet

class ConsultationViewSet(BaseCRUDViewSet):
    """
    A viewset for viewing and editing consultation instances.
    """
    queryset = ConsultationModel.objects.all()
    serializer_class = ConsultationSerializer
