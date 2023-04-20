from django.db import models
from rest_framework.viewsets import ModelViewSet

from . import serializers
from . import models


# show items of each user
class OwnedItemViewSet(ModelViewSet):
    def get_queryset(self):
        return models.OwnedItem.objects.filter(owner=self.request.user)

    serializer_class = serializers.OwnedItemSerializer


class PublicItemViewSet(ModelViewSet):
    queryset = models.OwnedItem.objects.filter(is_public=True)
    # allowed methods
    http_method_names = ['get']

    serializer_class = serializers.OwnedItemSerializer


class CrawledItemViewSet(ModelViewSet):
    queryset = models.CrawledItem.objects.all()
    # allowed methods
    http_method_names = ['get']

    serializer_class = serializers.CrawledItemSerializer
