from rest_framework import serializers
from django.db import models 
from .models import Module, Lesson,  UserCourseProgress
from courses.models import Course
from courses.serializer import CourseSerializer


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

    class Meta:
        model = UserCourseProgress
        fields = [ "progress_id","lesson", "isCompleted"]
        







