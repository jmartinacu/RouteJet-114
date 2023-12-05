from django.urls import path

from . import views

app_name = 'product'

urlpatterns = [
  path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
  path('<int:id>/<slug:slug>/review', views.rate, name='review'),   

]
