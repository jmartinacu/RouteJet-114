# core/views.py
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from core.forms import SignUpForm, LoginForm


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'core/register.html'  
    success_url = '/login/'

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'core/login.html' 
    success_url = '/profile/'
