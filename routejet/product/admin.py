from django.contrib import admin

# Register your models here.

from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available', 'start_date', 'end_date')
    list_filter = ('available', 'city', 'start_date', 'end_date' )
    list_editable = ('start_date', 'end_date', 'price', 'available')
    exclude = ['slug', ]
