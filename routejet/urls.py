from django.urls import path, include
from . import views
from django.contrib import admin

urlpatterns = [
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'), 
    path('login/', views.user_login, name='login'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
]
