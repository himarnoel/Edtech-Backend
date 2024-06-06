from rest_framework import serializers
from .models import Module, Lesson



class LessonSerializer(serializers.ModelSerializer):
    # Serializing all fields in the Lesson model
    class Meta:
        model = Lesson
        fields = '__all__'
        


class ModuleSerializer(serializers.ModelSerializer):
    # Nested serialization for lessons in a module
    lessons = LessonSerializer(many=True, read_only=True)
    class Meta:
        model = Module
        fields = '__all__'