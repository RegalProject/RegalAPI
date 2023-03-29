from rest_framework.viewsets import ModelViewSet
from django.db.models.signals import post_save
from django.dispatch import receiver
from . import models

from . import serializers
from . import models


class ProfileViewSet(ModelViewSet):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer


# make an empty profile after creating a user and set it to the user
@receiver(post_save, sender=models.CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        models.Profile.objects.create(user=instance)


