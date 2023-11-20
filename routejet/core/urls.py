from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from core.views import signup
from . import views
from .forms import LoginForm

app_name = 'core'

urlpatterns = [
    path('', views.home, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
]
