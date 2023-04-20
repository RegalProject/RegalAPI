from django.db.models.signals import post_save
from rest_framework.viewsets import ModelViewSet
from django.dispatch import receiver
from django.conf import settings
from . import serializers
from . import models

# show items of each user
class OwnedItemViewSet(ModelViewSet):
    def get_queryset(self):
        return models.OwnedItem.objects.filter(owner=self.request.user)

    serializer_class = serializers.OwnedItemSerializer