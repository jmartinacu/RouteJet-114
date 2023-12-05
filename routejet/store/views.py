from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.urls import reverse
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
from .utils import stripe_payment
from .tasks import task_send_email_order_created

from core.forms import OrderSearchForm

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
      task_send_email_order_created.delay(order.id)
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
        'error': { 'err': True, 'msg': 'No quedan tickets'}
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
        filter_arg = Q(city__icontains=query) | Q(name__icontains=query)

        try:
            # Attempt to convert the query to a float (for price)
            price_query = float(query)
            filter_arg |= Q(price=price_query) | Q(price__lte=price_query)
        except ValueError:
            pass

        results = Product.objects.filter(filter_arg)

    return render(request, 'store/product_filter.html', {'results': results, 'query': query})
def seguimiento(request):
  return render(request, 'store/order_search.html')

def search_order(request):
  query = request.GET.get('q')
  results = []
  if query:
    results = Order.objects.filter(Q(email__iexact=query) )
  return render(request, 'store/order_filter.html', {'results': results, 'query': query})

@login_required(login_url='/login')
def history(request):
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

  return render(request, 'store/history.html', {'orders': orders, 'form': form})

def getProductsbyOrders(orders):
    products=[]
    for order in orders:
        order_products= OrderItem.objects.filter(order=order)
        products=[product.product for product in order_products]
    return products

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/order_detail.html', {'order': order})
