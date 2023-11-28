from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from . import views

app_name = 'store'

urlpatterns = [
  path('', views.product_list, name='product_list'),
]



