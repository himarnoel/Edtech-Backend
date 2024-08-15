from rest_framework import serializers
from .models import Transaction, Enrollment
from courses.models import Course

class TransactionSerializer(serializers.ModelSerializer):
    courses = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), many=True
    )  # Handle multiple courses

    class Meta:
        model = Transaction
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    # transaction = TransactionSerializer(read_only=True)  # Optionally include transaction details

    class Meta:
        model = Enrollment
        fields = '__all__'
