from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from store.models import Order, OrderItem, Claim
from product.models import Product
from .models import Category, OrderItem
from .cart import Cart
from .forms import OrderCreateForm, AddProductForm, ClaimForm
from core.models import RouteJetUser
from .utils import stripe_payment

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
    results = Product.objects.filter(Q(city__icontains=query) )
  return render(request, 'core/product_filter.html', {'results': results, 'query': query})

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

@login_required
def create_claim(request):
    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            order_id = form.cleaned_data['order_id']
            claim_text = form.cleaned_data['claim_text']
            
            # Verifica si existe una orden con la ID proporcionada
            try:
                # Intenta obtener la orden, maneja la excepción si no se encuentra
                order = Order.objects.get(id=order_id)
            except Order.DoesNotExist:
                form.add_error('order_id', 'La orden no existe.')
                return render(request, 'store/create_claim.html', {'form': form})

             # Verifica que la orden esté relacionada con el usuario actual
            if order.email != request.user.email:
                form.add_error('order_id', 'La orden no está relacionada con el usuario actual.')
                return render(request, 'store/create_claim.html', {'form': form})
            
            # Verifica si ya existe una reclamación para la misma orden
            existing_claim = Claim.objects.filter(order=order).first()
            if existing_claim:
                form.add_error('order_id', 'Ya existe una reclamación para esta orden.')
                return render(request, 'store/create_claim.html', {'form': form})

            # Crea la reclamación utilizando la relación con Order
            claim = Claim(order=order, claim_text=claim_text)
            claim.save()

            return redirect('core:index')  # Puedes definir una URL de éxito
    else:
        form = ClaimForm()

    return render(request, 'store/create_claim.html', {'form': form})

@login_required
def claim_history(request):
    user_orders = Order.objects.filter(email=request.user.email)
    claims = Claim.objects.filter(order__in=user_orders)
    return render(request, 'store/claim_history.html', {'claims': claims})