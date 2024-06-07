from rest_framework import serializers
from .models import Transaction, Enrollment

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    # transaction = TransactionSerializer(read_only=True)  # Optionally include transaction details

    class Meta:
        model = Enrollment
        fields = '__all__'
