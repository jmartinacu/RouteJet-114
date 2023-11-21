from django.db import models

# Create your models here.

class Product(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images', blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    available = models.BooleanField(default=True)
    num_products = models.IntegerField(default=100)
   



    def save(self, *args, **kwargs):
        if self.num_products < 1:
            self.available = False
        super(Product, self).save(*args, **kwargs)
        if self.num_products > 1:
            self.available = True

class Meta:
    ordering = ('country', 'city', 'start_date', 'end_date')
    def __str__(self):
        return self.country + ' ' + self.city + ' ' + self.start_date + ' ' + self.end_date