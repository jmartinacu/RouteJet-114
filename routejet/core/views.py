# core/views.py
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from .forms import SignUpForm 
from django.shortcuts import render


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
