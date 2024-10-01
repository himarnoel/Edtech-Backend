from rest_framework import serializers
from django.db import models 
from .models import Module, Lesson,  CourseProgress
from courses.models import Course


class LessonSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = [
            'lesson_id',
            'title',
            'video_url',
            'pdf_file',
            'duration',
            'transcript',
            'module',
            'is_completed',
        ]

    def get_is_completed(self, lesson):
        # Check if the lesson is completed by the user
        user_progress = self.context.get('user_progress')
        if user_progress:
            return lesson in user_progress.completed_lessons.all()
        return False


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



class UserProgressSerializer(serializers.ModelSerializer):
    completed_lessons = LessonSerializer(many=True, context={})
    total_lessons = serializers.SerializerMethodField()
    total_completed_lessons = serializers.SerializerMethodField()

    class Meta:
        model = CourseProgress
        fields = [ "progress_id",'user', 'course', 'completed_lessons', 'total_lessons', 'total_completed_lessons']

    def get_total_lessons(self, obj):
        return obj.course.module.aggregate(total_lessons=models.Count('lessons'))['total_lessons'] or 0

    def get_total_completed_lessons(self, obj):
        return obj.completed_lessons.count()

    def to_representation(self, instance):
        self.fields['completed_lessons'].context['user_progress'] = instance
        return super().to_representation(instance)
