from django.shortcuts import get_object_or_404, render

from .models import Product
from store.forms import AddProductForm
from store.cart import Cart

def product_detail(request, id, slug):
  cart = Cart(request)
  product = get_object_or_404(Product, id=id, slug=slug, available=True)
  form = AddProductForm(cart=cart, product=product)
  return render(request, 'product/detail.html', {
    'product': product, 
    'form': form
  })
