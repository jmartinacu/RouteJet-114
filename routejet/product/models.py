from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete


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
    slug = models.SlugField(default='default-slug')

    def save(self, *args, **kwargs):
        if self.num_products < 1:
            self.available = False
        else:
            self.available = True

        if self.start_date > self.end_date:
            self.end_date = self.start_date

        super(Product, self).save(*args, **kwargs)


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
