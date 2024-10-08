from rest_framework import serializers
from .models import Transaction, Enrollment
from courses.models import Course
from courses.serializer import CourseSerializer




class TransactionSerializer(serializers.ModelSerializer):
    courses = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), many=True
    )  # Handle multiple courses

    class Meta:
        model = Transaction
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer()  # Nest CourseSerializer to include course details
  
    class Meta:
        model = Enrollment
        fields = ['enrollment_id', 'user', 'course', 'transaction','isPaid']
