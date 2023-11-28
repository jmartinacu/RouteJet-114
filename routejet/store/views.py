from django.views import View
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from product.models import Product
from .models import Category
from . import views

def product_list(request, category_slug=None): 
  category = None
  categories = Category.objects.all()
  products = Product.objects.filter(available=True)
  if category_slug:
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
  return render(request, 'store/product_list.html', {
    'products': products,
    'category': category,
    'categories': categories,
  })


def search_products(request):
  query = request.GET.get('q')
  results = []
  if query:
    results = Product.objects.filter(Q(city__icontains=query) )
  return render(request, 'core/product_filter.html', {'results': results, 'query': query})
