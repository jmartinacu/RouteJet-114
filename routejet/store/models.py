from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings
from decimal import *

class Order(models.Model):
    class ShipmentState(models.TextChoices):
        PREADMISSION = "PA", _("Pre-admisión")
        ONTHEWAY = "OTW", _("En camino")
        DELIVERED = "D", _("Entregado")

    class ShippingType(models.TextChoices):
       NORMAL = 'N', _('Normal')
       EXPRESS = 'E', _('Express')

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    paid = models.BooleanField(default=False)
    payment_on_delivery = models.BooleanField()
    stripe_id = models.CharField(max_length=250, blank=True)
    state = models.CharField(
        max_length=3, 
        choices=ShipmentState.choices, 
        default=ShipmentState.PREADMISSION
    )
    shipping_type = models.CharField(
        max_length=1,
        choices=ShippingType.choices,
        default=ShippingType.NORMAL,  
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created'])]

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        items_price = sum([item.get_cost() for item in self.items.all()])
        if self.shipping_type == self.ShippingType.EXPRESS:
            items_price += Decimal(settings.EXPRESS_SHIPMENT_PRICE)
        elif items_price < Decimal(settings.FREE_SHIPMENT_PRICE) and self.ShippingType.NORMAL == self.shipping_type:
            items_price += Decimal(settings.NORMAL_SHIPMENT_PRICE)
        return items_price
    
    def get_shipping_cost(self):
        shipping_cost = Decimal(0)
        if self.shipping_type == self.ShippingType.EXPRESS:
            shipping_cost += Decimal(settings.EXPRESS_SHIPMENT_PRICE)
        elif self.get_total_cost() < Decimal(settings.FREE_SHIPMENT_PRICE) and self.ShippingType.NORMAL == self.shipping_type:
            shipping_cost += Decimal(settings.NORMAL_SHIPMENT_PRICE)
        return shipping_cost
    

    def get_stripe_url(self):
        if not self.stripe_id:
            return ''
        if '_test_' in settings.STRIPE_SECRET_KEY:
            path = '/test/'
        else:
            path = '/'
        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'
        

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)


    def get_cost(self):
        return self.price * self.quantity


class Category(models.Model):
    country = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        if self.slug != self.country:
            self.slug = slugify(self.country)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        ordering = ['country']
        indexes = [models.Index(fields=['country'])]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

class Claim(models.Model):
    
    PENDING_REVIEW = 'Pending'
    IN_PROCESS = 'In Process'
    RESOLVED = 'Resolved'
    CLOSED = 'Closed'

    CLAIM_STATES = [
        (PENDING_REVIEW, 'Pendiente de revisión'),
        (IN_PROCESS, 'En proceso'),
        (RESOLVED, 'Resuelta'),
        (CLOSED, 'Cerrada'),
    ]

    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    claim_text = models.TextField()
    state = models.CharField(max_length=20, choices=CLAIM_STATES, default=PENDING_REVIEW)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Claim #{self.id} - Order #{self.order.id}"
    #Las reclamaciones se ordenan por fecha de creación en orden descendente
    class Meta:
        ordering = ['-created']
