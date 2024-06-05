# serializers.py
from rest_framework import serializers
from .models import Transaction, Enrollment

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['user', 'course', 'amount', 'reference', 'status', 'created_at']
        read_only_fields = ['reference', 'status', 'created_at']
        
        
class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['enrollment_id', 'user', 'course', 'transaction']
        read_only_fields = ['enrollment_id']
