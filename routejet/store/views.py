from store.models import Order, OrderProducts
from product.models import Product
from django.shortcuts import render, redirect, get_object_or_404
from .forms import OrderCreateForm
from django.views.decorators.http import require_POST
from .cart import Cart




def overview(request):
    cart=Cart(request)
    products=[product for product in cart]
    if request.user.is_authenticated:
       usuario=request.user
    else:
       usuario=None
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user=usuario
            for item in cart:
               order.add(item['product'], item['quantity'], item['price'])
            order.save()
            cart.clear()
            return render(request, 'store/overview.html', {"usuario":usuario, "productos":products,'form': form})
            
    else:
        form = OrderCreateForm()

    return render(request, 'store/overview.html', {"usuario":request.user, "productos":products,'form': form})

@require_POST
def cart_add(request, product_id):
  cart = Cart(request)
  product = get_object_or_404(Product, id=product_id)
  if cart[product_id]['quantity'] >= product.num_products:
    return render(request, 'store/cart.html', {
      'add_to_car_error': f'No hay suficientes viajes a {product.city}'
    })
  cart.add(product=product)
  return redirect('store:cart_detail')

@require_POST
def cart_remove(request, product_id):
  cart = Cart(request)
  product = get_object_or_404(Product, id=product_id)
  cart[product_id]['quantity'] -= 1
  if cart[product_id]['quantity'] == 0:
    cart.remove(product)
  return redirect('store:cart_detail')

def cart_detail(request):
  cart = Cart(request)
  return render(request, 'store/cart.html', { 'cart': cart })
