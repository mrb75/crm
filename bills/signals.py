from django.dispatch import Signal, receiver
from django.db.models.signals import post_save
from .models import Bill
from datetime import datetime
from .tasks import send_bill_creation_notification


@receiver(post_save, sender=Bill)
def set_bill_code(sender, **kwargs):
    current_id = kwargs['instance'].id
    if kwargs['created']:
        kwargs['instance'].code = 'vafa_{0}_{1}'.format(
            current_id, datetime.now().strftime('%Y%m%d%H%M%S'))
        kwargs['instance'].save()


@receiver(post_save, sender=Bill)
def send_bill_creation(sender, **kwargs):
    send_bill_creation_notification(kwargs['instance'])
