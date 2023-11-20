from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('',views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
        country_slug>/ <slug:category_slug>/<slug:subcategory_slug>/', views.product_list, name='product_list_by_subcategory'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),]