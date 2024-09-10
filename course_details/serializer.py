from rest_framework import serializers
from .models import Module, Lesson, VideoUpload, Video, Progress
from courses.models import Course


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields ="__all__"


class LessonSerializer(serializers.ModelSerializer):
    video = VideoSerializer(many=True, read_only=True)
    class Meta:
        model = Lesson
        fields = '__all__'


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



class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ['id', 'user', 'video', 'progress', 'completed']

class VideoUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoUpload
        fields = ('id', 'title', 'video')
