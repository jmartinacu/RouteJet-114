from store.models import Order, OrderProducts
from product.models import Product
from django.shortcuts import render

def overview(request):
    user_order=Order.objects.get(user=request.user)

    if user_order:
        order_products= OrderProducts.objects.filter(order=user_order)
        products=[product.product for product in order_products]
    else:
        products=[]
    return render(request, 'store/overview.html', {"usuario":request.user, "productos":products})