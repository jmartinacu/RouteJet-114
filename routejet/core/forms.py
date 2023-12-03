from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError

from .models import RouteJetUser

class LoginForm(AuthenticationForm):
  username = forms.CharField(widget=forms.TextInput(attrs={
    'placeholder': 'Usuario',
  }))

  password = forms.CharField(widget=forms.PasswordInput(attrs={
    'placeholder': 'Contraseña',
  }))

class SignUpForm(UserCreationForm):
  class Meta:
    model = RouteJetUser
    fields = ('username', 'email', 'password1', 'password2')

  email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

  username = forms.CharField(widget=forms.TextInput(attrs={
    'placeholder': 'Usuario',
  }))

  password1 = forms.CharField(widget=forms.PasswordInput(attrs={
    'placeholder': 'Contraseña',
  }))

  password2 = forms.CharField(widget=forms.PasswordInput(attrs={
    'placeholder': 'Repite tu contraseña',
  }))

class OrderSearchForm(forms.Form):
  search_query = forms.CharField(label='Buscar', required=False)