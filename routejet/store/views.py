from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from product.models import Product
from .models import Category, OrderItem
from .cart import Cart
from .forms import OrderCreateForm, AddProductForm
from core.models import RouteJetUser
from .utils import stripe_payment, reduce_order_num_products

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
        product_id = item['product'].id
        product = Product.objects.get(id=product_id)
        num_tickets = product.num_products - item['quantity']
        if num_tickets < 0:
          cart.remove(product)
          if num_tickets == 0:
            msg = f'No quedan tickets del {product.name}'
          else:
            msg = f'Solamente quedan {product.num_products} tickets del {product.name}'
          return render(request, 'store/cart.html', {
            'cart': cart,
            'error': { 'err': True, 'msg': msg}
          })
        OrderItem.objects.create(order=order, 
                                 product=item['product'], 
                                 price=item['price'], 
                                 quantity=item['quantity'])
      
      reduce_order_num_products(cart)
      cart.clear()
      if not order.payment_on_delivery:
        session = stripe_payment(request, order)
        return redirect(session.url, code=303)
      else: 
        return redirect('core:index')
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
  origin = request.GET.get('origin', None)
  product = get_object_or_404(Product, id=product_id)
  form = AddProductForm(request.POST, cart=cart, product=product)
  if form.is_valid():
    data = form.cleaned_data
    cart.add(product=product, quantity=data['quantity'])
    return redirect('store:cart_detail')
  else:
    if origin == 'detail':
      return render(request, 'product/detail.html', {
      'product': product,
      'form': form
      })
    elif origin == 'cart':
      return render(request, 'store/cart.html', {
        'cart': cart,
        'error': { 'err': True, 'msg': f'No quedan tickets del {product.name}'}
      })

@require_POST
def cart_remove(request, product_id):
  cart = Cart(request)
  product = get_object_or_404(Product, id=product_id)
  cart.cart[str(product.id)]['quantity'] -= 1
  if cart.cart[str(product.id)]['quantity'] == 0:
    cart.remove(product)
  return redirect('store:cart_detail')

def cart_detail(request):
  cart = Cart(request)
  return render(request, 'store/cart.html', { 
    'cart': cart,
    'error': { 'err': False, 'msg': None}
    })

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
