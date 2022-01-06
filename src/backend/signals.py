from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Provider
from django.contrib.auth.models import Group


@receiver(post_save, sender=Provider)
def create_group(sender, instance, created, **kwargs):
    """
    Signal to be run on Provider instance creation
    Creates a corresponding group for the Provider
    """
    if created:
        provider_abb = instance.providerabbr
        new_group, created = Group.objects.get_or_create(name=provider_abb)
        print(f"Group created: {provider_abb}")
