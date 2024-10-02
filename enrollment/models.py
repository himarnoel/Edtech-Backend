from django.db import models
from core.models import CustomUser
import uuid
from courses.models import Course



class Transaction(models.Model):
    reference = models.UUIDField(
        default=uuid.uuid4, editable=False, primary_key=True, unique=True
    )
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="transactions"
    )
    courses = models.ManyToManyField(
        Course, related_name="transactions"
    )  # Allows multiple courses per transaction
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.reference)


class Enrollment(models.Model):
    enrollment_id = models.UUIDField(
        default=uuid.uuid4, editable=False, primary_key=True, unique=True
    )
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="enrollments"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="enrollments"
    )
    transaction = models.ForeignKey(
        Transaction, on_delete=models.CASCADE, related_name="enrollments"
    )
    isPaid = models.BooleanField(default=False)

    class Meta:
        unique_together = (
            "user",
            "course",
        )  # Ensure unique enrollment per user and course

    def __str__(self):
        return str(self.enrollment_id)
