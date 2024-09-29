from django.db import models
from courses.models import Course
import uuid
import cloudinary.uploader  # Import uploader to handle file uploads
from .utils import get_video_duration  # Import the utility function
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
    video_url = CloudinaryField('video', resource_type='video', blank=True, null=True)
    pdf_file = CloudinaryField(
        'file', resource_type='raw', blank=True, null=True)
    duration = models.FloatField(
        help_text='Duration in seconds', default=0.0)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name='lessons')

    def save(self, *args, **kwargs):
        if self.video_url:
            upload_result = cloudinary.uploader.upload(
                self.video_url, resource_type='video')
            # Fetch the video duration from Cloudinary
            self.duration = upload_result['duration']
        
        if self.pdf_file:
            pdf_upload_result = cloudinary.uploader.upload( 
                self.pdf_file, resource_type='raw', access_mode='public')
            self.pdf_file = pdf_upload_result.get('url')+".pdf"  # Set the uploaded PDF URL
        super().save(*args, **kwargs)

   
    def __str__(self):
        return self.title



class CourseProgress(models.Model):
    progress_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    user = models.ForeignKey(CustomUser, related_name='progress', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_lessons = models.ManyToManyField(Lesson, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.course.title}"
