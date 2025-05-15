import logging
from django.db import IntegrityError
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from users.utils.generate_code import generate_code
from .utils.send_activation import send_code_email_activation

logger = logging.getLogger(__name__)
User = get_user_model()

@receiver(post_save, sender=User)
def send_activation_code_signal(sender, instance, created, **kwargs):

    if created and not instance.is_active:
        if not instance.email:
            logger.error(f"User (pk={instance.pk}) created without an email!")
            raise IntegrityError("Cannot send activation code: email not provided.")

        try:
            send_code_email_activation(instance)
            logger.info(f"Activation code sent to {instance.email}")
        except Exception as e:
            logger.error(f"Failed to send activation code to {instance.email}: {e}")
            raise ValueError(f"Failed to send activation code to {instance.email}: {e}")
