from django.db import models
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from . import serializers
from . import models
from . import filters


class ItemViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = filters.ItemFilter
    search_fields = ['name']


# show items of each user
class OwnedItemViewSet(ItemViewSet):
    serializer_class = serializers.OwnedItemSerializer
    filterset_class = filters.OwnedItemFilter

    def get_queryset(self):
        return models.OwnedItem.objects.filter(owner=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"user": self.request.user})
        return context


# get a users owned items by username
class OwnedItemByPKViewSet(ItemViewSet):
    queryset = models.OwnedItem.objects.all()
    serializer_class = serializers.OwnedItemSerializer
    # allowed methods
    http_method_names = ['get']
    
    def get_serializer(self, *args, **kwargs):
        return serializers.OwnedItemSerializer(many=True, *args, **kwargs)

    def get_object(self):
        return models.OwnedItem.objects.filter(owner__username=self.kwargs['pk'])


class PublicItemViewSet(ItemViewSet):
    queryset = models.OwnedItem.objects.filter(is_public=True)
    serializer_class = serializers.OwnedItemSerializer
    # allowed methods
    http_method_names = ['get']


class CrawledItemViewSet(ItemViewSet):
    queryset = models.CrawledItem.objects.all()
    serializer_class = serializers.CrawledItemSerializer
    filterset_class = filters.CrawledItemFilter
    # allowed methods
    http_method_names = ['get', 'post', 'delete', 'put']


# show recommended items
# add filters plz
class RecommendedItemViewSet(ModelViewSet):
    serializer_class = serializers.RecommendedItemSerializer
    # allowed methods
    http_method_names = ['get']

    def get_queryset(self):
        return models.RecommendedItem.objects.filter(user=self.request.user)


class RecommendedItemByPKViewSet(ModelViewSet):
    queryset = models.RecommendedItem.objects.all()
    serializer_class = serializers.RecommendedItemByPKSerializer
    # allowed methods
    http_method_names = ['get', 'put']

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(models.RecommendedItem, user__username=item)


class WishlistViewSet(ModelViewSet):
    serializer_class = serializers.WishlistSerializer
    # allowed methods
    http_method_names = ['get', 'patch']

    def get_queryset(self):
        return models.Wishlist.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"user": self.request.user})
        return context
    

class WishlistByPKViewSet(ModelViewSet):
    queryset = models.Wishlist.objects.all()
    serializer_class = serializers.WishlistByPKSerializer
    # allowed methods
    http_method_names = ['get']

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(models.RecommendedItem, user__username=item)
