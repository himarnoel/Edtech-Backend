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

            # Transcribe the video and set the transcript
            self.transcript = self.transcribe_video(self.video_url)

        # Now save the lesson after modifications are made
        super().save(*args, **kwargs)  # This should be called once


    def transcribe_video(self, video_url):
        if not video_url:
            return "No video URL provided."

        print(f"Transcribing video from URL: {video_url}")

        # Download the video file
        response = requests.get(video_url)
        if response.status_code == 200:
            # Create a temporary file to store the downloaded video
            temp_video_path = tempfile.mktemp(suffix=".mp4")
            with open(temp_video_path, 'wb') as temp_video:
                temp_video.write(response.content)

            # Extract audio from video
            audio_path = f"{temp_video_path}.wav"
            video_clip = VideoFileClip(temp_video_path)
            print(f"Audio path: {audio_path}")

            # Use a context manager to ensure the video clip is properly closed
            try:
                video_clip.audio.write_audiofile(audio_path)
            finally:
                video_clip.close()  # Ensure the video clip is closed

            # Transcribe audio
            recognizer = sr.Recognizer()
            try:
                with sr.AudioFile(audio_path) as source:
                    audio_data = recognizer.record(source)
                    transcript = recognizer.recognize_google(audio_data)  # Store transcript here
            except sr.UnknownValueError:
                transcript = "Could not understand the audio."
            except sr.RequestError as e:
                transcript = f"Could not request results from Google Speech Recognition service; {e}"
            # finally:
            #     # Clean up audio and temporary video files
            #     if os.path.exists(audio_path):
            #         # os.remove(audio_path)
            #     if os.path.exists(temp_video_path):
            #         os.remove(temp_video_path)

        else:
            transcript = "Failed to download video."

        return transcript  # Return the transcript, do not call self.save()
    
    def __str__(self):
        return self.title



class CourseProgress(models.Model):
    progress_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    user = models.ForeignKey(CustomUser, related_name='progress', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_lessons = models.ManyToManyField(Lesson, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.course.title}"
