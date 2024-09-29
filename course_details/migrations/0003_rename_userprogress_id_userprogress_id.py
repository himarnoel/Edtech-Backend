from django.db import migrations, models
import uuid

class Migration(migrations.Migration):

    dependencies = [
         ('course_details', '0002_rename_id_userprogress_userprogress_id'),  # Change this to your previous migration
    ]

    operations = [
        migrations.AlterField(
            model_name='userprogress',
            name='id',
            field=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False),
        ),
    ]
