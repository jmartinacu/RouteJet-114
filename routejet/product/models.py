from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.forms import ValidationError
from django.core.validators import MinValueValidator


class Product(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)])
    image = models.ImageField(upload_to='product_images', blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    available = models.BooleanField(default=True)
    num_products = models.IntegerField(default=100, validators=[MinValueValidator(0)])
    slug = models.SlugField(max_length=200,unique=True)

    def save(self, *args, **kwargs):
        if self.num_products < 1:
            self.available = False
        else:
            self.available = True
        
        super(Product, self).save(*args, **kwargs)

    
    def clean(self):
        super().clean()
        if self.start_date > self.end_date:
            raise ValidationError('La fecha de fin no puede ser anterior a la fecha de inicio.')



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

    
    class Meta:
        ordering = ['country', 'city', 'start_date']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['country']),
            models.Index(fields=['city']),
        ]

    def __str__(self):
        return f"{self.country} {self.city} {self.start_date} {self.end_date}"


