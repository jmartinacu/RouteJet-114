from store.models import Order, OrderProducts
from product.models import Product
from django.shortcuts import render
from .forms import OrderCreateForm

def overview(request):
    user_orders=Order.objects.filter(user=request.user)
    user_order=user_orders.first()
    if user_order:
        order_products= OrderProducts.objects.filter(order=user_order)
        products=[product.product for product in order_products]
    else:
        products=[]
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user 
            order.save() 
            order_products= OrderProducts.objects.filter(order=user_order)
            products=[product.product for product in order_products]
            for item in products:
                order.products.add(item)
            order.save()
            
    else:
        form = OrderCreateForm()

    return render(request, 'store/overview.html', {"usuario":request.user, "productos":products,'form': form})

def history(request):
    orders=Order.objects.filter(user=request.user)
    #orders = Order.objects.all()
    return render(request, 'store/history.html',{'orders':orders})
    #user_orders=Order.objects.filter(user=request.user)
    #return render(request, 'store/history.html', {"usuario":request.user, "ordenes":user_orders})

def getProductsbyOrders(orders):
    products=[]
    for order in orders:
        order_products= OrderProducts.objects.filter(order=order)
        products=[product.product for product in order_products]
    return products