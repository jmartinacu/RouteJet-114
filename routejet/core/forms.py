from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User 

from django import forms

class LoginForm(AuthenticationForm):
  username = forms.CharField(widget=forms.TextInput(attrs={
    'placeholder': 'Usuario',
  }))

  password = forms.CharField(widget=forms.PasswordInput(attrs={
    'placeholder': 'Contraseña',
  }))

class SignUpForm(UserCreationForm):
  class Meta:
    model = User
    fields = ('username', 'email', 'password1', 'password2')

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