from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
  path("create/", views.order_create, name="order_create"),
  path('cart/', views.cart_detail, name='cart_detail'),
  path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
  path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove')
]
