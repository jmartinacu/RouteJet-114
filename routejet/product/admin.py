from django.contrib import admin

# Register your models here.

from .models import Product

@admin.register(Product)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('country', 'city', 'start_date', 'end_date')
    list_filter = ('country', 'city', 'start_date', 'end_date', )
    search_fields = ('country', 'city', 'start_date', 'end_date',)
    ordering = ('country', 'city', 'start_date', 'end_date')
   