from rest_framework import serializers
from .models import ConsultationModel

class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationModel
        fields = '__all__'
