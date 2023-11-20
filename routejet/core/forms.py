from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
import re

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Nombre de usuario',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Contraseña',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Nombre de usuario',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'correo electrónico',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Contraseña',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repetir la contraseña',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
