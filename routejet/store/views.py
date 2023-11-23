from product.models import Product
from django.shortcuts import render

def product_catalog(request):
    products = Product.objects.all()
    return render(request, 'templates/catalog.html', {'products': products})

def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    return render(request, 'product/templates/product_detail.html', {'product': product})