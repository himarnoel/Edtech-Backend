from django.db import models
from core.models import CustomUser
import uuid
from courses.models import Course
# Create your models here.


class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='transactions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)




class Enrollment(models.Model):
    enrollment_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='enrollments')


