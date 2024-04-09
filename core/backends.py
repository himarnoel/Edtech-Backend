
from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class EmailVerificationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=username)
            if user.check_password(password) and user.email_verified:
                return user
        except CustomUser.DoesNotExist:
            pass
        return None