from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True) 
    fullName=models.CharField(max_length=200) 
    
    

class Meta:
    verbose_name_plural = 'Custom Users'

# Rename reverse accessors for CustomUser model
CustomUser.groups.field.remote_field.related_name = 'custom_user_groups'
CustomUser.user_permissions.field.remote_field.related_name = 'custom_user_permissions'