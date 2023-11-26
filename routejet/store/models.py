
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

    class ShippingType(models.TextChoices):
        NORMAL = 'NORMAL', _('Normal')
        EXPRESS = 'EXPRESS', _('Express')
        
    class ShippingPrice(models.DecimalField):
        NORMAL = 3.99
        EXPRESS = 7.99
        FREE_THRESHOLD = 400.00

    user = models.ForeignKey(RouteJetUser, on_delete=models.CASCADE, null=True)
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
    shipping_type = models.CharField(
        max_length=7,
        choices=ShippingType.choices,
        default=ShippingType.NORMAL,
    )

def save(self, *args, **kwargs):
    user = self.user
    self.total_price = 0
    if self.city is None:
        self.city = user.city
    if self.address is None:
        self.address = user.address
    super(Order, self).save(*args, **kwargs)
    for product in self.products.all():
        self.total_price += product.price

    # Calcula y asigna el precio de envío según el tipo seleccionado
    if self.total_price > ShippingPrice.FREE_THRESHOLD:
        self.shipping_price = 0.00
    elif self.shipping_type == ShippingType.NORMAL:
        self.shipping_price = ShippingPrice.NORMAL
    elif self.shipping_type == ShippingType.EXPRESS:
        self.shipping_price = ShippingPrice.EXPRESS
              
    self.total_price += self.shipping_price
    super(Order, self).save(*args, **kwargs)

class OrderProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
