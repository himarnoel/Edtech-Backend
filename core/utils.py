
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes


def send_verification_email(email, verification_token):
    subject = 'Verify Your Email Address'
    message = f'Please click the following link to verify your email: http://localhost:8000/api/verify-email/{verification_token}/'
    sender_email = settings.EMAIL_HOST_USER  # Use a sender email address from your domain
    recipient_list = [email]
    send_mail(subject, message, sender_email, recipient_list)
    

def send_resetPassword_email(user, token):
    reset_link = f" http://localhost:8000/api/reset-password/{urlsafe_base64_encode(force_bytes(user.pk))}/{token}/"
    send_mail(
            'Password Reset',
            f'Click the following link to reset your password: {reset_link}',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )