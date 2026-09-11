import secrets
from django.core.mail import EmailMessage
from gymflow import settings


def generate_verification_code():
    return str(secrets.randbelow(900000) + 100000)


def send_verification_email(email, code):
    try:
        print("called")
        email = EmailMessage(
            subject="Verification Email",
            body=f"Your verification code is: {code}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )
        email.send(fail_silently=False)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
