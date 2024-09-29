from django.core.management.base import BaseCommand
from course_details.models import UserProgress
import uuid

class Command(BaseCommand):
    help = 'Convert bigint userprogress_id to uuid'

    def handle(self, *args, **kwargs):
        # Check if there are any UserProgress instances to convert
        if not UserProgress.objects.exists():
            self.stdout.write(self.style.WARNING('No UserProgress entries found.'))
            return

        # Iterate over UserProgress objects and update their IDs
        for progress in UserProgress.objects.all():
            # If the id is a bigint, convert it to UUID
            # Assuming 'id' is the field you want to convert
            progress.id = uuid.uuid4()  # Generate a new UUID
            progress.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully converted {progress.id} to UUID.'))

        self.stdout.write(self.style.SUCCESS('All UserProgress entries converted to UUID.'))
