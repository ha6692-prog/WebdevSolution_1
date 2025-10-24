from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Doctor

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.is_doctor:
        Doctor.objects.get_or_create(user=instance)
