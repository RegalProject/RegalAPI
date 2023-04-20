from django.db import models
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404

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


# get a users owned items by username
class OwnedItemByPKViewSet(ModelViewSet):
    queryset = models.OwnedItem.objects.all()
    # allowed methods
    http_method_names = ['get']

    serializer_class = serializers.OwnedItemSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(models.OwnedItem, owner__username=item)


# show recomended items
class RecomendedItemViewSet(ModelViewSet):
    def get_queryset(self):
        return models.RecommendedItem.objects.filter(user=self.request.user)

    # allowed methods
    http_method_names = ['get']
    serializer_class = serializers.RecommendedItemSerializer