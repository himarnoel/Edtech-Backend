from django.db import models
from courses.models import Course
import uuid
from cloudinary.models import CloudinaryField

# Create your models here.


class Module(models.Model):
    module_id = models.UUIDField(
        default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='module')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.title




class Lesson(models.Model):
    lesson_id = models.UUIDField(
        default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    title = models.CharField(max_length=200)
    video_url = CloudinaryField('video', resource_type='video')  # Lesson content, can include text, links, video URLs, etc.
    lesson_details=models.TextField(),
    order = models.PositiveIntegerField(default=0) 
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    
    def __str__(self):
        return self.title