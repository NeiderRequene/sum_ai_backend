from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(
        verbose_name='email address', max_length=255, unique=True)
    register_type = models.CharField(max_length=20, default='email')
    is_verify_email = models.BooleanField(default=False)

    # Settings to authenticate via email
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
