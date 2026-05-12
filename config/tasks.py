from datetime import datetime

from celery import shared_task
from django.core.mail import send_mail


@shared_task
def add(x, y):
    return x + y


@shared_task
def send_gmail(mail, message):
    send_mail(
        subject=message,
        message=message,
        from_email="giyosoripov4@gmail.com",
        recipient_list=[mail],
    )


@shared_task
def print_time():
    now = datetime.now()
    print(f'vaqt {now}')
