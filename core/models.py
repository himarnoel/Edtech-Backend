
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager
from django.db import models
import uuid


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_staff being True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser being True")

        return self.create_user(email=email, password=password, **extra_fields)



class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    fullName = models.CharField(max_length=200)
    email_verified = models.BooleanField(default=False)
    accept_terms_and_conditions = models.BooleanField(default=False)
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


# class Meta:
#     verbose_name_plural = 'Custom Users'


# # Rename reverse accessors for CustomUser model
# CustomUser.groups.field.remote_field.related_name = 'custom_user_groups'
# CustomUser.user_permissions.field.remote_field.related_name = 'custom_user_permissions'
