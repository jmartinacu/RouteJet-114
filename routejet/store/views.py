from store.models import Order, OrderProducts
from product.models import Product
from django.shortcuts import render, redirect, get_object_or_404
from .forms import OrderCreateForm
from django.views.decorators.http import require_POST
from .cart import Cart



def overview(request):
    user_orders = Order.objects.filter(user=request.user)
    user_order = user_orders.first()

    if user_order:
        order_products = OrderProducts.objects.filter(order=user_order)
        products = [product.product for product in order_products]
    else:
        products = []

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            # Actualiza el tipo de envío de la orden
            order.shipping_type = form.cleaned_data['shipping_type']
            order.save()

            order_products = OrderProducts.objects.filter(order=user_order)
            products = [product.product for product in order_products]

            for item in products:
                order.products.add(item)

            order.save()

    else:
        form = OrderCreateForm()

    return render(request, 'store/overview.html', {"usuario": request.user, "productos": products, 'form': form})


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
