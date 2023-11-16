from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from core.models import UserProfile
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _


class SignUpForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = [ 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ocultar las restricciones por defecto
        for field_name in ['email', 'password1', 'password2']:
            self.fields[field_name].help_text = ''

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        # Validar la contraseña manualmente y mostrar los errores personalizados
        try:
            password_validation.validate_password(password1, self.instance)
        except forms.ValidationError as error:
            self.add_error('password1', error)
        return password1

class LoginForm(AuthenticationForm):
    email = forms.EmailField(
        label=_("Correo electrónico"),
        widget=forms.EmailInput(attrs={'autofocus': True}),
    )

    class Meta:
        model = UserProfile
        fields = ['email', 'password']