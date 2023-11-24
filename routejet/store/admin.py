from django.contrib import admin

from .models import Order, OrderProducts

class OrderProductInLine(admin.TabularInline):
  model = OrderProducts
  extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
  inlines = (OrderProductInLine,)
  list_display = ('user', 'total_price', 'state', 'city', 'address')
  readonly_fields = ('total_price',)
  exclude = ('stripe_payment',)

admin.site.register(OrderProducts)