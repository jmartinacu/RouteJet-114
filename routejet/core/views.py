# core/views.py
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from store.cart import Cart

from .forms import SignUpForm 

def home(request):
  cart = Cart(request)
  return render(request, 'core/index.html',{"usuario":request.user, 'cart': cart})

def signup(request):
  cart = Cart(request)
  if request.method == 'POST':
    form = SignUpForm(request.POST)

    if form.is_valid():
      form.save()
      return redirect('/login/' )
  else:
    form = SignUpForm()

  return render(request, 'core/signup.html', {
    'form': form,
    'cart': cart,
  })

def logout_view(request):
  logout(request)
  return redirect('/')

