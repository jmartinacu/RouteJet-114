from django.urls import path

from . import views
from .views import order_detail

app_name = 'store'

urlpatterns = [
  path('', views.product_list, name='product_list'),
  path('<slug:category_slug>', views.product_list, name='product_list_by_category'),
  path('search/', views.search_products, name='search_products'),
  path('searchOrder/', views.search_order, name='search_order'),
  path("create/", views.order_create, name="order_create"),
  path('cart/', views.cart_detail, name='cart_detail'),
  path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
  path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
  path('payment/completed', views.payment_completed, name='payment_completed'),
  path('payment/canceled', views.payment_canceled, name='payment_canceled'),
  path('seguimiento/',views.seguimiento,name='seguimiento'),
  path('order/<int:order_id>/', order_detail, name='order_detail'),
]
