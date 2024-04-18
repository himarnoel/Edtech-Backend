from django.db import models
from django.contrib.auth.models import User
import uuid
from courses.models import Course
# Create your models here.


class Transaction(models.Model):
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=False)



class Enrollment(models.Model):
    enrollment_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='enrollments')


