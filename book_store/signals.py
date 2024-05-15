from django.db.models.signals import post_save

from django.contrib.auth.models import User
from django.dispatch import receiver

from book_store.models import GuestProfile


@receiver(post_save, sender=User)
def create_guestprofile(sender, instance, created, **kwargs):
    if created:
        GuestProfile.objects.create(user=instance)
