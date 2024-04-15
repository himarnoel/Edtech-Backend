from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from rest_api_payload import success_response, error_response

baseURL="https://haelsoft-elearning-fe.vercel.app"
def send_verification_email(email, verification_token):
    subject = 'Verify Your Email Address'
    from_email = settings.EMAIL_HOST_USER  # Use a sender email address from your domain
    to_email = email
    
    # Render email template with context
    html_content = render_to_string('verification_email.html', {'verification_link': f'{baseURL}/verified?token={verification_token}/','useremail': email})
    
    email = EmailMultiAlternatives(subject, '', from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=True)
 
    

def send_resetPassword_email(user, token):
    subject = 'Password Reset'
    from_email = settings.EMAIL_HOST_USER  # Use a sender email address from your domain
    to_email = user.email
    
    
    reset_link = f" {baseURL}/auth/api/reset-password/{urlsafe_base64_encode(force_bytes(user.pk))}/{token}/"
    
    html_content = render_to_string("resetpassword.html",{"reset_link":reset_link,'useremail': user.email, "userName":user.fullName})
    
    
    
    
    
    email = EmailMultiAlternatives(subject, '', from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=True)
    
def error_message(message):
    payload=error_response(
            status="Failed",
            message=message
    )
    return payload

def success_message(data, message):
    payload= success_response(
                status="Success",
                message=message, 
                data=data    
            )
    return payload