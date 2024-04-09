
from django.core.mail import send_mail
from django.conf import settings


def send_verification_email(email, verification_token):
    subject = 'Verify Your Email Address'
    message = f'Please click the following link to verify your email: http://localhost:8000/api/verify-email/{verification_token}/'
    sender_email = settings.EMAIL_HOST_USER  # Use a sender email address from your domain
    recipient_list = [email]
    send_mail(subject, message, sender_email, recipient_list)