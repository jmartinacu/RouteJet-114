from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.product_list),
    path('search/', views.search_products, name='search_products'),
]



