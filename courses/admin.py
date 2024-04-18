from django.contrib import admin
from .models import Category, Subcategory, Course

# Registering the models
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Course)