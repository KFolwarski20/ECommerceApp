from io import BytesIO
from celery import shared_task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order


@shared_task
def payment_completed(order_id):
    """
    Task send the email notification after a successful order.
    """
    order = Order.objects.get(id=order_id)
    # Create email message with the bill.
    subject = 'My shop - bill no {}'.format(order.id)
    message = 'In the attachment you can find the bill from last shopping.'
    email = EmailMessage(subject, message, 'admin@myshop.com', [order.email])
    # PDF generation.
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    # Attach the PDF file
    email.attach('order_{}.pdf'.format(order.id), out.getvalue(), 'application/pdf')
    # Send the email
    email.send()
