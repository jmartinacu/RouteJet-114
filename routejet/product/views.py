from django.shortcuts import get_object_or_404, render

from .models import Product

def product_detail(request, id, slug):
  product = get_object_or_404(Product, id=id, slug=slug, available=True)
  return render(request, 'product/detail.html', {'product': product})