
from django.db import models
from django.urls import reverse
class Product(models.Model):

    # ...
    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.id, self.slug])

