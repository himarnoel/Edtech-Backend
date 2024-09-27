from rest_framework import serializers
from .models import CorporateInquiryModel


class CorporateInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = CorporateInquiryModel
        fields = '__all__'
