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
    completed = models.BooleanField(default=False)

    def update_completion_status(self):
        lessons = self.lessons.all()
        completed_lessons = lessons.filter(progress__completed=True).count()
        self.completed = lessons.count() == completed_lessons
        self.save()

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

    def update_completion_status(self):
        videos = self.video.all()
        completed_videos = videos.filter(progress__completed=True).count()
        self.completed = videos.count() == completed_videos
        self.save()
        # Update the parent module status
        self.module.update_completion_status()

    def __str__(self):
        return self.title


class Video(models.Model):
    lesson = models.ForeignKey(
        Lesson, related_name='video', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video = CloudinaryField('video', resource_type='video')
    duration = models.FloatField(
        help_text='Duration in seconds', default=0.0, )
    progress = models.FloatField(default=0, help_text='Progress in seconds')
    completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):

        if self.video:
            # Extract public ID from video URL
            upload_result = cloudinary.uploader.upload(
                self.video, resource_type='video')

            # Fetch the video duration from Cloudinary
            self.duration = upload_result['duration']
       
            

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class CourseProgress(models.Model):
    course = models.OneToOneField(
        Course, related_name='course_progress', on_delete=models.CASCADE)
    progress_percentage = models.FloatField(
        default=0, help_text='Total progress percentage of the course')
    completed = models.BooleanField(default=False)

    def update_progress(self):
        videos = Video.objects.filter(lesson__module__course=self.course)
        total_duration = sum(video.duration for video in videos)
        total_progress = sum(
            min(video.progress, video.duration) for video in videos
            if video.progress is not None
        )

        if total_duration > 0:
            self.progress_percentage = (total_progress / total_duration) * 100
        else:
            self.progress_percentage = 0

        self.completed = self.progress_percentage >= 100
        self.save()

    def __str__(self):
        return f'{self.user.email} - {self.course.title}'
