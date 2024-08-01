from django.contrib import admin
from .models import Category, Course



# Registering the models
admin.site.register(Category)
admin.site.register(Course)
