from django.urls import path

from . import views
from . import webhooks

app_name = 'store'

urlpatterns = [
  path('', views.product_list, name='product_list'),
  path('<slug:category_slug>', views.product_list, name='product_list_by_category'),
  path('search/', views.search_products, name='search_products'),
  path("cart/create/", views.order_create_with_cart, name="order_create_with_cart"),
  path("create/<int:product_id>/", views.order_create_without_cart, name="order_create_without_cart"),
  path('order/search/', views.search_order, name='search_order'),
  path('cart/', views.cart_detail, name='cart_detail'),
  path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
  path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
  path('payment/completed', views.payment_completed, name='payment_completed'),
  path('payment/canceled', views.payment_canceled, name='payment_canceled'),
  path('webhook/', webhooks.stripe_webhook, name='stripe_webhook'),
  path('order/tracking/',views.tracking,name='tracking'),
  path('order/<int:order_id>/', views.order_detail, name='order_detail'),
  path('create_claim/', views.create_claim, name='create_claim'),
  path('claim_history/', views.claim_history, name='claim_history'),
  path('history/', views.history, name='history'),

]
