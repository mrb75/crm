from django.dispatch import Signal, receiver
from django.db.models.signals import post_delete, post_save
from .models import UserImage, User
from .tasks import send_user_info_after_creation


@receiver(post_delete, sender=UserImage)
def user_image_delete(sender, **kwargs):
    # print(kwargs)
    kwargs['instance'].path.storage.delete(kwargs['instance'].path.name)


@receiver(post_save, sender=User)
def user_created(sender, **kwargs):
    send_user_info_after_creation(kwargs['instance'])
