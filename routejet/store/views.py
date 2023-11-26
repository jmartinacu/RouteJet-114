from django.shortcuts import render, redirect
from .forms import OrderCreateForm
from .models import Order, OrderProducts

def overview(request):
    user_orders = Order.objects.filter(user=request.user)
    user_order = user_orders.first()

    if user_order:
        order_products = OrderProducts.objects.filter(order=user_order)
        products = [product.product for product in order_products]
    else:
        products = []

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            # Actualiza el tipo de envío de la orden
            order.shipping_type = form.cleaned_data['shipping_type']
            order.save()

            order_products = OrderProducts.objects.filter(order=user_order)
            products = [product.product for product in order_products]

            for item in products:
                order.products.add(item)

            order.save()

    else:
        form = OrderCreateForm()

    return render(request, 'store/overview.html', {"usuario": request.user, "productos": products, 'form': form})
