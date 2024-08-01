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




class Course(models.Model):
    course_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    title = models.CharField(max_length=200)
    image = models.CharField(max_length=255, default="https://firebasestorage.googleapis.com/v0/b/web-project-ca895.appspot.com/o/haelsoft%2Fcourse2.png?alt=media&token=dc1bc361-eefb-4963-87b9-c449213f1ea0" )
    description = models.TextField(max_length=800,unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    creation_date = models.DateTimeField(auto_now_add=True)
   
    
    def __str__(self):
        return self.title




