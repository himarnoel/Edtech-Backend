# Generated by Django 5.1 on 2024-09-28 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_details', '0011_remove_video_lesson_lesson_duration_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
