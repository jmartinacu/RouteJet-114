from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

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
    fields = ('username', 'email', 'first_name', 'last_name', 'city', 'address', 'postal_code', 'password1', 'password2')

  username = forms.CharField(widget=forms.TextInput(attrs={
    'placeholder': 'Usuario',
  }))

  email = forms.EmailField(max_length=254, help_text='Necesario. Añada una cuenta de email valida.')

  first_name = forms.CharField(max_length=250, help_text='Añada su nombre.')
    
  last_name = forms.CharField(max_length=250, help_text='Añada su apellido.')

  city = forms.CharField(max_length=250, help_text='Añada su ciudad de residencia.')

  address = forms.CharField(max_length=250, help_text='Añada su dirección de residencia.')

  postal_code = forms.IntegerField(min_value=0, help_text='Añada su codigo postal.')

  password1 = forms.CharField(widget=forms.PasswordInput(attrs={
    'placeholder': 'Contraseña',
  }))

  password2 = forms.CharField(widget=forms.PasswordInput(attrs={
    'placeholder': 'Repite tu contraseña',
  }))

class OrderSearchForm(forms.Form):
  search_query = forms.CharField(label='', required=False)