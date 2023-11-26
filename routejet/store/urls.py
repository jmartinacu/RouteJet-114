from django.urls import path

<<<<<<< HEAD
app_name = 'store'

urlpatterns = []
=======
from . import views

app_name = 'store'

urlpatterns = [
  path('cart/', views.cart_detail, name='cart_detail'),
  path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
  path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove')
]
>>>>>>> feature/5-shopping_cart
