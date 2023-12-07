from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class RouteJetUserManager(BaseUserManager):
  def create_user(self, username, email, password=None):
    if not username:
      raise ValueError('An username is required')
    if not password:
      raise ValueError('A password is required')
    email = self.normalize_email(email)
    user = self.model(username=username, email=email)
    user.set_password(password)
    user.save()
    return user

  def create_superuser(self, username, email, password=None):
    if not username:
      raise ValueError('An username is required')
    if not password:
      raise ValueError('A password is required')
    user = self.create_user(username, email, password)
    user.is_superuser = True
    user.is_staff = True
    user.save()
    return user

class RouteJetUser(AbstractBaseUser, PermissionsMixin):
  user_id = models.AutoField(primary_key=True)
  username = models.CharField(max_length=50, unique=True)
  email = models.EmailField(max_length=50, unique=True)
  first_name = models.CharField(max_length=30, null=True)
  last_name = models.CharField(max_length=30, null=True)
  city = models.CharField(max_length=100, null=True)
  address = models.CharField(max_length=100, null=True)
  postal_code = models.CharField(max_length=10, null=True)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)
  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['email']
  objects = RouteJetUserManager()
  def __str__(self) -> str:
    return self.username
