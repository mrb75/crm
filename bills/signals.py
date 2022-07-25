from django.dispatch import Signal, receiver
from django.db.models.signals import post_save
from .models import Bill
from datetime import datetime


@receiver(post_save, sender=Bill)
def set_bill_code(sender, **kwargs):
    current_id = kwargs['instance'].id
    bill = Bill.objects.get(pk=current_id)
    bill.code = 'vafa_{0}_{1}'.format(
        current_id, datetime.now().strftime('%Y%m%d%H%M%S'))
