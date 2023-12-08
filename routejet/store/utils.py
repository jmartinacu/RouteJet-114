from decimal import Decimal
import stripe
from django.conf import settings
from django.urls import reverse

from product.models import Product
from .models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def reduce_order_num_products_cart(cart):
    for item in cart:
        product_id = item['product'].id
        product = Product.objects.get(id=product_id)
        product.num_products = product.num_products - item['quantity']
        product.save()


def reduce_order_num_products_not_cart(product_id, quantity):
    product = Product.objects.get(id=product_id)
    product.num_products = product.num_products - int(quantity)
    product.save()


def stripe_payment(request, order):
    success_url = request.build_absolute_uri(
        reverse('store:payment_completed'))
    cancel_url = request.build_absolute_uri(reverse('store:payment_canceled'))
    session_data = {
        'mode': 'payment',
        'client_reference_id': order.id,
        'success_url': success_url,
        'cancel_url': cancel_url,
        'line_items': [],
        'shipping_options': [
            {
                'shipping_rate_data': {
                    'type': 'fixed_amount',
                    'fixed_amount': {
                        'amount': int(order.get_shipping_cost() * Decimal(100)), 'currency': 'eur'
                    },
                    'display_name': Order.ShippingType(order.shipping_type).label
                }
            }
        ]
    }
    for item in order.items.all():
        session_data['line_items'].append({
            'price_data': {
                'unit_amount': int(item.price * Decimal('100')),
                'currency': 'eur',
                'product_data': {
                    'name': item.product.city,
                },
            },
            'quantity': item.quantity
        })
    session = stripe.checkout.Session.create(**session_data)
    return session
