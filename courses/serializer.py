from rest_framework import serializers
from .models import Category,  Course, CourseReview
# from course_details.serializer import ModuleSerializer



class CourseSerializer(serializers.ModelSerializer):
    # module=ModuleSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = '__all__'  # Serialize all fields in the Course model
        

class CourseReviewSerializer(serializers.ModelSerializer):
     course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
     user = serializers.ReadOnlyField(source='user.email')
     class Meta:
        model = CourseReview
        fields = ['coursereview_id', 'course', 'rating', 'comment', 'user',]
        read_only_fields = ['user']

class CategorySerializer(serializers.ModelSerializer):
    # Nested serializers courses
    courses = CourseSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = '__all__'  # Serialize all fields in the Category model
