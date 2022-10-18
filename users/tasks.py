from celery import shared_task
from .models import Turn, Notification
from django.utils import timezone
from datetime import timedelta


@shared_task(name='send_turn_message')
def send_turn_message():
    time_threshold = timezone.now()+timedelta(hours=3)
    turns = Turn.objects.filter(date_visit__lte=time_threshold)
    notifications = []
    for item in turns:
        notifications.append(Notification(
            text='you have an appointment at {}'.format(item.visit_date_time),
            user=item.user,
        ))
        # send messages

    Notification.objects.bulk_create(notifications)


@shared_task
def send_user_info_after_creation(user):
    Notification.objects.create(
        user=user, text="wellcome to our crm, your username is {0}.".format(user.username))
    # send message
