from rest_framework import serializers
from .models import Category,  Course
from course_details.serializer import ModuleSerializer


class CourseSerializer(serializers.ModelSerializer):
    module=ModuleSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = '__all__'  # Serialize all fields in the Course model
        




class CategorySerializer(serializers.ModelSerializer):
    # Nested serializers for subcategories and courses
    course = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'  # Serialize all fields in the Category model
