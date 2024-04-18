from django.db import models
from courses.models import Course
import uuid

# Create your models here.


class Module(models.Model):
    module_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)


class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    video_url = models.TextField()  # Lesson content, can include text, links, video URLs, etc.
    lesson_details=models.CharField(max_length=200),
    order = models.PositiveIntegerField(default=0) 