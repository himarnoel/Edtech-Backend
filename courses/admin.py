from django.contrib import admin
from .models import Category, Subcategory, Course
from course_details.models import Lesson, Module


# Registering the models
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Module)