# core/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class UserProfile(AbstractUser):
    additional_field = models.CharField(max_length=30, blank=True)

    class Meta:
        swappable = 'AUTH_USER_MODEL'
