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


# get a users owned items by username
class OwnedItemByPKViewSet(ModelViewSet):
    queryset = models.OwnedItem.objects.all()

    # allowed methods
    http_method_names = ['get']
    serializer_class = serializers.OwnedItemSerializer

    def get_serializer(self, *args, **kwargs):
        return serializers.OwnedItemSerializer(many=True, *args, **kwargs)

    def get_object(self):
        return models.OwnedItem.objects.filter(owner__username=self.kwargs['pk'])


class PublicItemViewSet(ModelViewSet):
    queryset = models.OwnedItem.objects.filter(is_public=True)
    # allowed methods
    http_method_names = ['get']

    serializer_class = serializers.OwnedItemSerializer


class CrawledItemViewSet(ModelViewSet):
    queryset = models.CrawledItem.objects.all()
    # allowed methods
    http_method_names = ['get', 'post', 'delete', 'put']

    serializer_class = serializers.CrawledItemSerializer


# show recommended items
class RecommendedItemViewSet(ModelViewSet):
    def get_queryset(self):
        return models.RecommendedItem.objects.filter(user=self.request.user)

    # allowed methods
    http_method_names = ['get']
    serializer_class = serializers.RecommendedItemSerializer


class RecommendedItemByPKViewSet(ModelViewSet):
    queryset = models.RecommendedItem.objects.all()

    # allowed methods
    http_method_names = ['get', 'put']
    serializer_class = serializers.RecommendedItemByPKSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(models.RecommendedItem, user__username=item)


class WishlistViewSet(ModelViewSet):
    def get_queryset(self):
        return models.Wishlist.objects.filter(user=self.request.user)

    # allowed methods
    http_method_names = ['get', 'post', 'delete']

    serializer_class = serializers.WishlistSerializer


class WishlistByPKViewSet(ModelViewSet):
    queryset = models.Wishlist.objects.all()

    # allowed methods
    http_method_names = ['get']

    serializer_class = serializers.WishlistByPKSerializer

    def get_object(self):
        return models.Wishlist.objects.filter(user=self.kwargs['pk'])
