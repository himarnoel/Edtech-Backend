from rest_framework import serializers
from django.db import models 
from .models import Module, Lesson,  UserCourseProgress
from courses.models import Course



class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields ='__all__'

  


class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    class Meta:
        model = Module
        fields = '__all__'


class CourseContentSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, source='module')

    class Meta:
        model = Course
        fields = ['title', 'modules', "course_id"]



class UserCourseProgressSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()
    completed_lessons = LessonSerializer(many=True, read_only=True)
    progress_percentage = serializers.FloatField(read_only=True)

    class Meta:
        model = UserCourseProgress
        fields = "__all__"

    def get_course(self, obj):
        from courses.serializer import CourseSerializer  # Lazy import
        return CourseSerializer(obj.course).data


