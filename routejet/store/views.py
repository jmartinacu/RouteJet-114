from product.models import Product
from django.forms import SlugField
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.db.models import Q
from . import views


def product_list(request): 
    products = Product.objects.all()
    return render(request, 'core/product_list.html', {'products': products})


from django.shortcuts import render


def search_products(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Product.objects.filter(Q(city__icontains=query) )
    return render(request, 'core/product_filter.html', {'results': results, 'query': query})

