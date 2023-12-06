from typing import Any
from django import forms

from .models import Order
from product.models import Product
from .cart import Cart

class OrderCreateForm(forms.ModelForm):
  class Meta:
    model=Order
    fields=['first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'payment_on_delivery','shipping_type']

class AddProductForm(forms.Form):
  quantity = forms.IntegerField(min_value=0, initial=1, label='Cantidad')

  def __init__(self, *args, **kwargs):
    self.cart = kwargs.pop('cart', None)
    self.product = kwargs.pop('product', None)
    super(AddProductForm, self).__init__(*args, **kwargs)

  def clean(self):
    cart = self.cart
    product = self.product
    cleaned_data = super().clean()
    quantity = cleaned_data.get('quantity')
    cart_product = cart.cart.get(str(product.id), {'quantity': 0})
    if (int(quantity) + cart_product['quantity']) > product.num_products:
      if product.num_products - cart_product["quantity"] == 0:
        msg = 'No quedan tickets'
      else:
        msg =  f'Solamente quedan { product.num_products - cart_product["quantity"]} tickets'
      self.add_error('quantity', msg)
    return cleaned_data

class ClaimForm(forms.Form):
    order_id = forms.IntegerField(label="Id Reclamación", widget=forms.TextInput(attrs={'class': 'form-control'}))
    claim_text = forms.CharField(label="Descripcion", widget=forms.Textarea(attrs={'class': 'form-control'}))