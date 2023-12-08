from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.forms import ValidationError
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from django.urls import reverse

from core.models import RouteJetUser

class Product(models.Model):
    category = models.ForeignKey('store.Category', related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, auto_created=True)
    image = models.ImageField(upload_to='products/', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)])
    available = models.BooleanField(default=True)
    num_products = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if self.num_products < 1:
            self.available = False
        else:
            self.available = True
        if self.slug != self.name:
          self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)


    def clean(self):
        super().clean()
        if self.start_date > self.end_date:
            raise ValidationError('La fecha de fin no puede ser anterior a la fecha de inicio.')

    class Meta:
        ordering = ['name', 'city', 'start_date']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("product:product_detail", args=[self.id, self.slug])
    def get_absolute_url2(self):
        return reverse("product:review", args=[self.id, self.slug])
    
    
    
@receiver(post_delete, sender=Product)
def post_save_image(sender, instance, **kwargs):
    """ Clean Old Image file """
    try:
        instance.image.delete(save=False)
    except:
        pass

    try:
        instance.img.delete(save=False)
    except:
        pass

class Review(models.Model):
    user=models.ForeignKey(RouteJetUser,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    description=models.CharField(max_length=200)
    valoration=models.IntegerField()

    def __str__(self):
        return str(self.user.username)
