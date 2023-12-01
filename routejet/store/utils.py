from decimal import Decimal
import stripe
from django.conf import settings
from django.urls import reverse

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

def stripe_payment(request, order):
  success_url = request.build_absolute_uri(reverse('store:payment_completed'))
  cancel_url = request.build_absolute_uri(reverse('store:payment_canceled'))
  session_data = {
    'mode': 'payment',
    'client_reference_id': order.id,
    'success_url': success_url,
    'cancel_url': cancel_url,
    'line_items': []
  }
  for item in order.items.all():
    session_data['line_items'].append({
      'price_data': {
        'unit_amount': int(item.price * Decimal('100')),
        'currency': 'usd',
        'product_data': {
          'name': item.product.city,
        },
      },
      'quantity': item.quantity
    })
  session = stripe.checkout.Session.create(**session_data)
  return session
  
