from django.core.mail import send_mail
from celery import shared_task
from django.conf import settings

from store.models import Order
from routejet.celery import app

@shared_task
def task_send_email_order_created(order_id):
  order = Order.objects.get(id=order_id)
  subject = f'Pedido nr. {order.id}'
  message = f'Estimado cliente {order.first_name}, \n\n' \
            f'Tu pedido ha sido completado correctamente.\n' \
            f'El ID de tu pedido es {order.id}, puedes ver los detalles del pedido con tu email en el historial de pedidos.'
  mail_sent = send_mail(subject, message, settings.EMAIL_HOST_USER, [order.email])
  return mail_sent

@app.task
def task_change_state_orders_every_day():
  orders = Order.objects.exclude(state='D')
  for order in orders:
    if order.state == 'PA' and order.paid:
      order.state = 'OTW'
      order.save()
    elif order.paid:
      order.state = 'D'
      order.save()
  return 'success'
  