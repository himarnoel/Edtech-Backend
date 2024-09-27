# Generated by Django 5.1 on 2024-09-12 10:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_details', '0007_remove_lesson_order_remove_module_order'),
        ('courses', '0006_remove_coursereview_id_coursereview_coursereview_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress_percentage', models.FloatField(default=0, help_text='Total progress percentage of the course')),
                ('completed', models.BooleanField(default=False)),
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='course_progress', to='courses.course')),
            ],
        ),
        migrations.RemoveField(
            model_name='progress',
            name='user',
        ),
        migrations.RemoveField(
            model_name='progress',
            name='video',
        ),
        migrations.DeleteModel(
            name='VideoUpload',
        ),
        migrations.AddField(
            model_name='module',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='video',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='video',
            name='progress',
            field=models.FloatField(default=0, help_text='Progress in seconds'),
        ),
        migrations.DeleteModel(
            name='Progress',
        ),
    ]