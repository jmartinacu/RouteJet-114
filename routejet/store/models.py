from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse

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
  stripe = models.BooleanField()
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
  product = models.ForeignKey('product.Product', related_name='order_items', on_delete=models.CASCADE)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  quantity = models.PositiveIntegerField(default=1)

  def __str__(self) -> str:
    return str(self.id)
  
  def get_cost(self):
    return self.price * self.quantity

class Category(models.Model):
  country = models.CharField(max_length=200)
  slug = models.SlugField(max_length=200, unique=True)

  def save(self, *args, **kwargs) -> None:
    if self.slug != self.country:
      self.slug = slugify(self.country)
    super(Category, self).save(*args, **kwargs)

  class Meta:
    ordering = ['country']
    indexes = [
       models.Index(fields=['country'])
    ]
    verbose_name = 'category'
    verbose_name_plural = 'categories'
  
  def __str__(self) -> str:
     return self.country
  
  def get_absolute_url(self):
      return reverse("store:product_list_by_category", args=[self.slug])
  

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
