from django.conf import settings
from decimal import Decimal

from product.models import Product



class Cart:
  def __init__(self, request ,shipping_type=None) -> None:
    """ 
    Initialize the cart
    """
    self.session = request.session
    cart = self.session.get(settings.CART_SESSION_ID)
    if not cart:
      cart = self.session[settings.CART_SESSION_ID] = {}
    self.cart = cart
    
    self.shipping_type = shipping_type 

  def add(self, product, quantity=1, override_quantity=False):
    product_id = str(product.id)
    if product_id not in self.cart:
      self.cart[product_id] = {
        'quantity': 0,
        'price': str(product.price)
      }
    if override_quantity:
      self.cart[product_id]['quantity'] = quantity
    else:
      self.cart[product_id]['quantity'] += quantity
    self.save()

  def save(self):
    self.session.modified = True
  
  def remove(self, product):
    product_id = str(product.id)
    if product_id in self.cart:
      del self.cart[product_id]
      self.save()
  
  def __iter__(self):
    product_ids = self.cart.keys()
    products = Product.objects.filter(id__in=product_ids)
    cart = self.cart.copy()
    for product in products:
      cart[str(product.id)]['product'] = product
    for item in cart.values():
      item['price'] = Decimal(item['price'])
      item['total_price'] = item['price'] * item['quantity']
      yield item
  
  def __len__(self):
    return sum(item['quantity'] for item in self.cart.values())

  def get_total_price(self):
    return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
  
  def get_total_cost_with_delivery(self, shipping_type):
          total_cost = self.get_total_price()

          if shipping_type == Order.ShippingType.EXPRESS:
              total_cost += 7.99
          elif shipping_type == Order.ShippingType.NORMAL and total_cost < 400:
              total_cost += 3.99

          return total_cost
  
  def clear(self):
    del self.session[settings.CART_SESSION_ID]
    self.save()
  
  def len(self):
    return self.__len__()
  
