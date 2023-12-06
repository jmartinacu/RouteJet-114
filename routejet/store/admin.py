from django.contrib import admin

from .models import Order, OrderItem
from .models import Category

class OrderItemInLine(admin.TabularInline):
  model = OrderItem
  raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
  list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid', 'state', 'created', 'updated']
  list_filter = ['paid', 'state', 'created', 'updated']
  inlines = [OrderItemInLine]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  list_display = ['country', 'slug']
  exclude = ['slug', ]

