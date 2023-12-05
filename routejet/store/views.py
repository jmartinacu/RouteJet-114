from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from store.models import Order, OrderItem
from product.models import Product
from .models import Order
from .models import Category, OrderItem
from .cart import Cart
from .forms import OrderCreateForm, AddProductForm
from core.models import RouteJetUser
from .utils import stripe_payment, reduce_order_num_products_cart, reduce_order_num_products_not_cart
from .tasks import task_send_email_order_created

from core.forms import OrderSearchForm

def get_or_none(classmodel, **kwargs):
  try:
    return classmodel.objects.get(**kwargs)
  except:
    return None

def order_create_without_cart(request, product_id):
  cart = Cart(request)
  product = Product.objects.get(id=product_id)
  quantity = request.GET.get('quantity', None)
  if quantity == '':
    quantity = 1
  if request.method == 'POST':
    form = OrderCreateForm(request.POST)
    if form.is_valid():
      product_db = Product.objects.get(id=product_id)
      num_tickets = product_db.num_products - int(quantity)
      if num_tickets < 0:
        if num_tickets == 0:
          msg = f'No quedan tickets del {product.name}'
        else:
          msg = f'Solamente quedan {product.num_products} tickets del {product.name}'
        return render(request, 'store/cart.html', {
          'cart': cart,
          'error': { 'err': True, 'msg': msg}
        })
      order = form.save()
      OrderItem.objects.create(order=order, 
                                product=product, 
                                price=product.price, 
                                quantity=1)
      reduce_order_num_products_not_cart(product.id, quantity)
      # task_send_email_order_created.delay(order.id)
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
    print('Quantity: ', quantity)
    return render(request, 'store/overview_without_cart.html', {
      'cart': cart,
      'product': product, 
      'quantity': quantity, 
      'form': form,
    })


def order_create_with_cart(request):
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
          order.delete()
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
      
      reduce_order_num_products_cart(cart)
      # task_send_email_order_created.delay(order.id)
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
  cart = Cart(request)
  return render(request, 'store/completed.html', {'cart': cart})

def payment_canceled(request):
  cart = Cart(request)
  return render(request, 'store/canceled.html', {'cart': cart})

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
  request.session.modified = True
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
  cart = Cart(request)
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
    'cart': cart,
  })


def search_products(request):
  query = request.GET.get('q')
  cart = Cart(request)
  results = []
  if query:
    results = Product.objects.filter(Q(city__icontains=query) )
  return render(request, 'core/product_filter.html', {'results': results, 'query': query, 'cart': cart})

def tracking(request):
  cart = Cart(request)
  return render(request, 'store/order_search.html', {'cart': cart})

def search_order(request):
  cart = Cart(request)
  query = request.GET.get('q')
  results = []
  if query:
    results = Order.objects.filter(Q(email__iexact=query) )
  return render(request, 'store/order_filter.html', {'results': results, 'query': query, 'cart': cart})

@login_required(login_url='/login')
def history(request):
  cart = Cart(request)
  form = OrderSearchForm(request.GET)
  orders = Order.objects.filter(email=request.user.email)

  if form.is_valid():
      search_query = form.cleaned_data['search_query']
      if search_query:
            state_mapping = dict(Order.ShipmentState.choices)
            orders = orders.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(city__icontains=search_query) |
                Q(address__icontains=search_query) |
                Q(state__in=[k for k, v in state_mapping.items() if v.lower().startswith(search_query.lower())]) |  # Buscar por opciones legibles
                Q(id__icontains=search_query)
            )

  return render(request, 'store/history.html', {'orders': orders, 'form': form, 'cart': cart})

def getProductsbyOrders(orders):
    products=[]
    for order in orders:
        order_products= OrderItem.objects.filter(order=order)
        products=[product.product for product in order_products]
    return products

def order_detail(request, order_id):
    cart = Cart(request)
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/order_detail.html', {'order': order, 'cart': cart})
