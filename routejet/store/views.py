from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .cart import Cart
from store.models import Order, OrderItem
from product.models import Product
from .forms import OrderCreateForm
from core.models import RouteJetUser

def get_or_none(classmodel, **kwargs):
  try:
    return classmodel.objects.get(**kwargs)
  except:
    return None

def order_create(request):
  cart = Cart(request)
  if request.method == 'POST':
    form = OrderCreateForm(request.POST)
    if form.is_valid():
      order = form.save()
      for item in cart:
        OrderItem.objects.create(order=order, 
                                 product=item['product'], 
                                 price=item['price'], 
                                 quantity=item['quantity'])
      cart.clear()
      return redirect('core:index')
  else:
    user = get_or_none(RouteJetUser, username=request.user.username)
    if user == None:
      form = OrderCreateForm()
    else: 
      form = OrderCreateForm({'email' : user.email, 'address' : user.address, 'city' : user.city})
    return render(request, 'store/overview.html', {'cart': cart, 'form': form})

# def overview(request):
#     user_orders=Order.objects.filter(user=request.user)
#     user_order=user_orders.first()
#     if user_order:
#         order_products= OrderProducts.objects.filter(order=user_order)
#         products=[product.product for product in order_products]
#     else:
#         products=[]
#     if request.method == 'POST':
#         form = OrderCreateForm(request.POST)
#         if form.is_valid():
#             order = form.save(commit=False)
#             order.user = request.user 
#             order.save() 
#             order_products= OrderProducts.objects.filter(order=user_order)
#             products=[product.product for product in order_products]
#             for item in products:
#                 order.products.add(item)
#             order.save()
            
#     else:
#         form = OrderCreateForm()

    # return render(request, 'store/overview.html', {"usuario":request.user, "productos":products,'form': form})

@require_POST
def cart_add(request, product_id):
  cart = Cart(request)
  product = get_object_or_404(Product, id=product_id)
  if cart[product_id]['quantity'] >= product.num_products:
    return render(request, 'store/cart.html', {
      'cart': cart,
      'add_to_car_error': f'No hay suficientes viajes a {product.city}',
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
