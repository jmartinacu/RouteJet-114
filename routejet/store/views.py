from product.models import Product
from django.forms import SlugField
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views


def product_list(request): 
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

