from django.db import models
from courses.models import Course
import uuid
import cloudinary.uploader  # Import uploader to handle file uploads
from .utils import get_video_duration  # Import the utility function
from cloudinary.models import CloudinaryField
from core.models import CustomUser
import cloudinary.uploader
import speech_recognition as sr
import os
from moviepy.editor import VideoFileClip
from django.core.files.temp import NamedTemporaryFile
import requests
import tempfile


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
    video_url = CloudinaryField('video', resource_type='video', blank=True, null=True)
    pdf_file = CloudinaryField(
        'file', resource_type='raw', blank=True, null=True)
    duration = models.FloatField(
        help_text='Duration in seconds', default=0.0)
    transcript = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name='lessons')

    def save(self, *args, **kwargs):
        if self.video_url:
            # Upload the video to Cloudinary
            upload_result = cloudinary.uploader.upload(
                self.video_url, resource_type='video')
            self.video_url = upload_result['secure_url']
            print(upload_result)

            # Fetch the video duration from Cloudinary
            self.duration = upload_result['duration']

        # Now save the lesson after modifications are made
        super().save(*args, **kwargs)  # This should be called once



    def __str__(self):
        return self.title



class UserCourseProgress(models.Model):
    progress_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    user = models.ForeignKey(CustomUser, related_name='progress', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson,null=True, related_name='progress',on_delete=models.CASCADE)
    isCompleted=models.BooleanField(default=False)

    class Meta:
        unique_together=["user","lesson"]

   
    def __str__(self):
        return f"{self.user.email} - {self.lesson}"
