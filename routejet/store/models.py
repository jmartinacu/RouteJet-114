from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import RouteJetUser
from product.models import Product

class StripePayment(models.Model):
  stripe_checkout_id = models.CharField(max_length=500)
  payment_bool = models.BooleanField(default=False)

class Order(models.Model):
  class ShipmentState(models.TextChoices):
    PREADMISSION = "PA", _("Pre-admisión")
    ONTHEWAY = "OTW", _("En camino")
    DELIVERED = "D", _("Entregado")

  user = models.ForeignKey(RouteJetUser, on_delete=models.CASCADE)
  products = models.ManyToManyField(Product, related_name='product', through='OrderProducts')
  stripe_payment = models.ForeignKey(StripePayment, on_delete=models.CASCADE, null=True)
  total_price = models.DecimalField(decimal_places=2, max_digits=6)
  state = models.CharField(
    max_length=3, 
    choices=ShipmentState.choices, 
    default=ShipmentState.PREADMISSION
  )
  city = models.CharField(max_length=100)
  address = models.CharField(max_length=100)

  def save(self, *args, **kwargs):
    if self.city == None:
      self.city = self.user.city
    if self.address == None:
      self.address = self.user.address
    self.total_price = 0.00
    super(Order, self).save(*args, **kwargs)
    products = self.products.all()
    for product in self.products.all():
      self.total_price += product.price
    super(Order, self).save(*args, **kwargs)

class OrderProducts(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  order = models.ForeignKey(Order, on_delete=models.CASCADE)


