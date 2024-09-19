from django.contrib import admin

# Register your models here.
from .models import Lesson, Module, Video, CourseProgress


# Registering the models

admin.site.register(Lesson)
admin.site.register(Module)
admin.site.register(Video)
admin.site.register(CourseProgress)
