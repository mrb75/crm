from celery import shared_task
from users.models import Notification


@shared_task()
def send_bill_creation_notification(bill):
    message_text = 'your bill created successfully.thank you for.'
    Notification.objects.create(text=message_text, user=bill.user)
