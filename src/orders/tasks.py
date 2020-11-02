from celery import task
from django.core.mail import send_mail
from .models import Order


@task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = "thành công đã đặt hàng xong"
        # f'Dear {order.first_name}, \n\n' f'You have successfully ' \
        #       f'placed an order.' f'Your order ID is {order.id}.'
    mail_sent = send_mail(subject, message, 'tuantt1889@gmail.com',
                          [order.email])
    return mail_sent