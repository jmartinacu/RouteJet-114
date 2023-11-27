from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from core.views import signup, logout_view
from store.views import overview, history, order_detail
from . import views
from .forms import LoginForm

app_name = 'core'

urlpatterns = [
    path('', views.home, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
    path('logout/',logout_view, name='logout'),
    path('overview/', overview, name='overview'),
    path('history/', history, name='history'),
    path('order/<int:order_id>/', order_detail, name='order_detail'),
]