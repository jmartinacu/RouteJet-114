from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
import re

class LoginForm(AuthenticationForm):
  username = forms.CharField(widget=forms.TextInput(attrs={
    'placeholder': 'Usuario',
  }))

  password = forms.CharField(widget=forms.PasswordInput(attrs={
    'placeholder': 'Contraseña',
  }))

class SignUpForm(UserCreationForm):
  email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

  username = forms.CharField(widget=forms.TextInput(attrs={
    'placeholder': 'Usuario',
  }))

  email = forms.CharField(widget=forms.EmailInput(attrs={
    'placeholder': 'Email',
  }))

  password1 = forms.CharField(widget=forms.PasswordInput(attrs={
    'placeholder': 'Contraseña',
  }))

  password2 = forms.CharField(widget=forms.PasswordInput(attrs={
    'placeholder': 'Repite tu contraseña',
  }))
