from .models import Order
from django import forms

class OrderCreateForm(forms.ModelForm):
    class Meta:
            model=Order
            fields=['user','city','address','phone','email','stripe_payment']