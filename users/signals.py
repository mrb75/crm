from django.dispatch import Signal, receiver
from django.db.models.signals import post_delete
from .models import UserImage


@receiver(post_delete, sender=UserImage)
def user_image_delete(sender, **kwargs):
    # print(kwargs)
    kwargs['instance'].path.storage.delete(kwargs['instance'].path.name)
