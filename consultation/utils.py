from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string


def send_consult_email_user(email, name):
    subject = 'Consultation Signup Confirmation'
    # Use a sender email address from your domain
    from_email = settings.EMAIL_HOST_USER
    to_email = email

    # Render email template with context
    html_content = render_to_string(
        "useremail.html", {'name': name, 'useremail': email})
  
    email = EmailMultiAlternatives(subject, '', from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=True)


def send_consult_email_admin(email, phone_number, name):
    subject = 'New Consultation Signup'
    # Use a sender email address from your domain
    from_email = settings.EMAIL_HOST_USER
    to_email = email

    # Render email template with context
    html_content = render_to_string(
        "adminemail.html", {'name': name, 'email': email, "phone_number": phone_number})

    email = EmailMultiAlternatives(subject, '', from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=True)
