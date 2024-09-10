from django.db import models
from courses.models import Course
import uuid
from cloudinary.models import CloudinaryField
from core.models import CustomUser

# Create your models here.


class Module(models.Model):
    module_id = models.UUIDField(
        default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='module')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    lesson_id = models.UUIDField(
        default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    title = models.CharField(max_length=200)
    sample_video_url = CloudinaryField('video', resource_type='video')
    lesson_details = models.TextField(),
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name='lessons')

    def __str__(self):
        return self.title


class VideoUpload(models.Model):
    title = models.CharField(max_length=255)
    video = CloudinaryField('video', resource_type='video')

    def __str__(self):
        return self.title


class Video(models.Model):
    lesson = models.ForeignKey(
        Lesson, related_name='video', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video = CloudinaryField('video', resource_type='video')
    duration = models.FloatField(help_text='Duration in seconds')

    def __str__(self):
        return self.title


class Progress(models.Model):
    user = models.ForeignKey(
        CustomUser, related_name='progress', on_delete=models.CASCADE)
    video = models.ForeignKey(
        Video, related_name='progress', on_delete=models.CASCADE)
    progress = models.FloatField(default=0, help_text='Progress in seconds')
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.email} - {self.video.title}'