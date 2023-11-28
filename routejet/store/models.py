from collections.abc import Iterable
from django.db import models
from django.utils.text import slugify

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

# class Product(models.Model):

#     # ...
#     def get_absolute_url(self):
#         return reverse('store:product_detail', args=[self.id, self.slug])

