from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User
from chat.consumers import notify_user


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        notify_user(1, f'user {instance.username} registratsiyadan otdi')
