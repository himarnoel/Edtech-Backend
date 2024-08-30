from django.contrib import admin

# Register your models here.
from .models import Lesson, Module,VideoUpload


# Registering the models

admin.site.register(Lesson)
admin.site.register(Module)
admin.site.register(VideoUpload)