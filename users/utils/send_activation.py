import logging
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.exceptions import ValidationError

from .generate_code import generate_code

logger = logging.getLogger(__name__)

def send_code_email_activation(instance):
    try:
        code, signed = generate_code(instance.email, "activate")

        send_mail(
            subject="Activation Code",
            message=f"Your activation code is: {code}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.email],
        )

        logger.info(f"Activation code sent to {instance.email}")
    except Exception as e:
        logger.error(f"Error sending activation code: {e}")
        raise ValidationError(f"Error sending activation code: {e}")



def send_code_email_reset_password(instance):
    try:
        code, signed = generate_code(instance.email, "reset")

        send_mail(
            subject="Reset Password Code",
            message=f"Your activation Reset Password code is: {code}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.email],
        )

        logger.info(f"Activation Reset Password code sent to {instance.email}")
    except Exception as e:
        logger.error(f"Error sending activation reset password code: {e}")
        raise ValidationError(f"Error sending activation reset password code: {e}")