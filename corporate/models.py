from django.db import models
import uuid


class CorporateInquiryModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, editable=False, unique=True)
    name = models.CharField(max_length=255)
    email_address = models.EmailField(unique=True)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    need = models.TextField()

    def __str__(self):
        return self.name
