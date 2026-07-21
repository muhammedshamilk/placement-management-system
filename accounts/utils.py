import random
from django.core.mail import send_mail
from django.conf import settings


def generate_otp():
    """
    Generate a random 6-digit OTP.
    """
    return str(random.randint(100000, 999999))


def send_otp_email(email, otp):
    """
    Send OTP email to user.
    """

    subject = "PlacementHub Password Reset OTP"

    message = f"""
Hello,

Your PlacementHub password reset OTP is:

{otp}

This OTP is valid for 5 minutes.

If you did not request a password reset, please ignore this email.

Regards,
PlacementHub Team
"""

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )