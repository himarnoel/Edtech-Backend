from django.db import models
import uuid
from cloudinary.models import CloudinaryField

# Create your models here.
class BlogPost(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    image=CloudinaryField('image', resource_type='image', blank=True, null=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title