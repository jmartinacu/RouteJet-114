# core/views.py
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import logout

from .forms import SignUpForm 

def home(request):
  return render(request, 'core/index.html',{"usuario":request.user})

def signup(request):
  if request.method == 'POST':
    form = SignUpForm(request.POST)

    if form.is_valid():
      form.save()
      return redirect('/login/' )
  else:
    form = SignUpForm()

  return render(request, 'core/signup.html', {
    'form': form
  })

def logout_view(request):
  logout(request)
  return redirect('/')
