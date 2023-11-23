from django.shortcuts import get_object_or_404, render
from .models import Product
# Create your views here.

def product_list(request): 
    products = Product.objects.all()
    return render(request, 'catalogo/product_list.html', {'products': products})

def product_detail(request,id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
   
    return render(request, 'catalogo/product_detail.html', {'product': product})