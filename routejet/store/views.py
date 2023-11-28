from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from product.models import Product
from .models import Category

from .cart import Cart
from store.models import Order, OrderItem
from product.models import Product
from .forms import OrderCreateForm
from core.models import RouteJetUser
from .utils import stripe_payment

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
      if order.stripe:
        session = stripe_payment(request, order)
        return redirect(session.url, code=303)
      else: 
        return redirect(reverse('core:index'))
  else:
    user = get_or_none(RouteJetUser, username=request.user.username)
    if user == None:
      form = OrderCreateForm()
    else: 
      form = OrderCreateForm(initial={'email' : user.email, 'address' : user.address, 'city' : user.city})
    return render(request, 'store/overview.html', {'cart': cart, 'form': form})

def payment_completed(request):
  return render(request, 'store/completed.html')

def payment_canceled(request):
  return render(request, 'store/canceled.html')

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
