from django.db.models.signals import post_save
from django.dispatch import receiver
from closet.models import Wishlist, RecommendedItem
from . import models


# make an empty profile after creating a user and set it to the user
@receiver(post_save, sender=models.CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        models.Profile.objects.create(user=instance)


# make an empty wishlist after creating a user and set it to the user
@receiver(post_save, sender=models.CustomUser)
def create_wishlist(sender, instance, created, **kwargs):
    if created:
        Wishlist.objects.create(user=instance)


@receiver(post_save, sender=models.CustomUser)
def create_recommended_list(sender, instance, created, **kwargs):
    if created:
        RecommendedItem.objects.create(user=instance)
