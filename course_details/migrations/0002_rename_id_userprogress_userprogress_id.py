# Generated by Django 5.1 on 2024-09-29 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course_details', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprogress',
            old_name='id',
            new_name='userprogress_id',
        ),
    ]