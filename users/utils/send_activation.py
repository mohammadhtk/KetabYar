import logging
from django.core.mail import send_mail
from django.conf import settings
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
        # ثبت لاگ خطا
        logger.error(f"Error sending activation code: {e}")
