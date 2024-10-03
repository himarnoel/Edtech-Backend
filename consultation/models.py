from django.db import models
import uuid
from django.utils import timezone

class ConsultationModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    name = models.CharField(max_length=255,unique=False)
    email = models.EmailField(unique=False)
    phone_number = models.CharField(max_length=15,unique=False)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
