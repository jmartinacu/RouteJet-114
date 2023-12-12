# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from store.cart import Cart

from product.models import Product
from .forms import SignUpForm


def home(request):
    cart = Cart(request)
    featured_cities = [
        'Viaje a Barcelona',
        'Viaje a Madrid',
        'Viaje a Sevilla'
    ]
    featured_products = Product.objects.filter(name__in=featured_cities)
    return render(request, 'core/index.html', {
        'cart': cart,
        'featured_products': featured_products
    })


def signup(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:
        form = SignUpForm()

    return render(request, 'core/signup.html', {
        'form': form,
        'cart': cart,
    })


def logout_view(request):
    logout(request)
    return redirect('/')
