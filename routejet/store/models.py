from django.db import models
from django.utils.translation import gettext_lazy as _

from product.models import Product

class Order(models.Model):
  class ShipmentState(models.TextChoices):
    PREADMISSION = "PA", _("Pre-admisión")
    ONTHEWAY = "OTW", _("En camino")
    DELIVERED = "D", _("Entregado")
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  email = models.EmailField()
  city = models.CharField(max_length=100)
  address = models.CharField(max_length=250)
  postal_code = models.CharField(max_length=20)
  paid = models.BooleanField(default=False)
  state = models.CharField(
    max_length=3, 
    choices=ShipmentState.choices, 
    default=ShipmentState.PREADMISSION
  )
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ['-created']
    indexes = [
      models.Index(fields=['-created'])
    ]
  
  def __str__(self) -> str:
    return f'Order {self.id}'
  
  def get_total_cost(self):
    return sum([item.get_cost() for item in self.items.all()])

class OrderItem(models.Model):
  order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
  product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  quantity = models.PositiveIntegerField(default=1)

  def __str__(self) -> str:
    return str(self.id)
  
  def get_cost(self):
    return self.price * self.quantity

