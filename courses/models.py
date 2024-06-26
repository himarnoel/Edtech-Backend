from django.db import models
from core.models import CustomUser
import uuid

# Create your models here.
# This is for the display


class Category(models.Model):
    category_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    name=models.CharField(max_length=200,unique=True)
    
    def __str__(self):
        return self.name    




class Subcategory(models.Model):
    subcategory_id = models.UUIDField(default=uuid.uuid4,  primary_key=True, editable=False, unique=True)
    name = models.CharField(max_length=100,unique=True)
    description = models.TextField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    
    def __str__(self):
        return self.name




class Course(models.Model):
    course_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=255,unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    creation_date = models.DateTimeField(auto_now_add=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='course')
    
    def __str__(self):
        return self.title




