# Generated by Django 5.1 on 2024-09-29 18:53

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_remove_course_image_course_video_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='img_course',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
    ]
