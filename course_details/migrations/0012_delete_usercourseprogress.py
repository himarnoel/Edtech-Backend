# Generated by Django 5.1 on 2024-10-21 00:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course_details', '0011_rename_progress_id_usercourseprogress_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserCourseProgress',
        ),
    ]
