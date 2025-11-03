from celery import shared_task
from django.core.mail import send_mail
from .models import Order


@shared_task
def order_created(order_id):
    """Task to send the notification email after a successful creating order object."""
    order = Order.objects.get(id=order_id)
    subject = 'Order number {}'.format(order_id)
    message = ('Hello, {}!\n\nYou made the order in our shop. Order Id is {}.'.format(order.first_name,
                                                                                        order.id))
    mail_sent = send_mail(subject, message, 'admin@myshop.com', [order.email])
    return mail_sent
