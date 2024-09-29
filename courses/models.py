from django.db import models
from cloudinary.models import CloudinaryField
from core.models import CustomUser
import uuid
import cloudinary.uploader


# Create your models here.
# This is for the display


class Category(models.Model):
    category_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    course_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    title = models.CharField(max_length=200)
    img_course=CloudinaryField('image', resource_type='image', blank=True, null=True)
    video_url = CloudinaryField('video', resource_type='video', blank=True, null=True)
    description = models.TextField(max_length=800, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class CourseReview(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    )
    coursereview_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    user = models.ForeignKey(
        CustomUser, related_name='reviews', on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()

    def __str__(self):
        return f"{self.course} <-> {self.rating} <-> {self.comment}"
