import random
from datetime import timezone, timedelta

from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models
from datetime import datetime
import uuid

# Create your models here.



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        if not password:
            raise ValueError('User must have a password')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


# upload profile image to media/users/profile_images
def profile_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'profiles/{datetime.now().strftime("%Y/%m/%d")}/{uuid.uuid4().hex}.{ext}'

class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.ImageField(upload_to=profile_image_upload_path, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    notifications_enabled = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email

