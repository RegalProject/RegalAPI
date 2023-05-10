from django.db import models
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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
    permission_classes = [IsAuthenticated]

    # allowed methods
    http_method_names = ['get', 'post', 'delete', 'patch']

    def get_queryset(self):
        return models.OwnedItem.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):

        if not 100 >= int(request.data['score']) >= 0:
            return Response({'error': 'score must be between 0 and 100'}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        if 'score' in request.data:
            if not 100 >= int(request.data['score']) >= 0:
                return Response({'error': 'score must be between 0 and 100'}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        return serializer.save(owner=self.request.user)


# get a users owned items by username
class OwnedItemByPKViewSet(ItemViewSet):
    queryset = models.OwnedItem.objects.all()
    # allowed methods
    http_method_names = ['get']
    
    def get_serializer(self, *args, **kwargs):
        return serializers.OwnedItemSerializer(many=True, *args, **kwargs)

    # def get_object(self):
    #     return models.OwnedItem.objects.filter(owner__username=self.kwargs['pk'])

    def list(self, request, *args, **kwargs):
        return Response({'error': 'list not allowed'}, status.HTTP_400_BAD_REQUEST)


class PublicItemViewSet(ItemViewSet):
    queryset = models.OwnedItem.objects.filter(is_public=True)
    serializer_class = serializers.OwnedItemSerializer
    # allowed methods
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        return Response({'error': 'only detailed retrieve allowed'}, status=status.HTTP_400_BAD_REQUEST)


class CrawledItemViewSet(ItemViewSet):
    queryset = models.CrawledItem.objects.all()
    serializer_class = serializers.CrawledItemSerializer
    filterset_class = filters.CrawledItemFilter
    # allowed methods
    http_method_names = ['get', 'post', 'delete', 'put']


# show recommended items
class RecommendedItemViewSet(ItemViewSet):
    serializer_class = serializers.CrawledItemSerializer
    filterset_class = filters.CrawledItemFilter
    permission_classes = [IsAuthenticated]
    # allowed methods
    http_method_names = ['get']

    def get_queryset(self):
        return models.RecommendedItem.objects.get(user=self.request.user).items.all()


class RecommendedItemByPKViewSet(ModelViewSet):
    queryset = models.RecommendedItem.objects.all()
    serializer_class = serializers.RecommendedItemByPKSerializer
    # allowed methods
    http_method_names = ['get', 'put']

    # def get_object(self, queryset=None, **kwargs):
    #     item = self.kwargs.get('pk')
    #     return get_object_or_404(models.RecommendedItem, user__username=item)


class WishlistViewSet(ItemViewSet):
    serializer_class = serializers.WishlistSerializer
    filterset_class = filters.CrawledItemFilter
    permission_classes = [IsAuthenticated]
    # allowed methods
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        return models.Wishlist.objects.get(user=self.request.user).items.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.CrawledItemSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.CrawledItemSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = serializers.CrawledItemSerializer(instance)
        return Response(serializer.data)

    def get_object(self):
        return self.get_queryset().get(pk=self.kwargs['pk'])

    # append item to the users wishlist
    def create(self, request, *args, **kwargs):
        wishlist = models.Wishlist.objects.get(user=self.request.user)
        data = dict()
        data['user'] = self.request.user.id
        data['items'] = []
        data['items'].extend(self.request.data['items'])

        serializer = serializers.WishlistSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        wishlist.items.add(data['items'][0])
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        wishlist = models.Wishlist.objects.get(user=self.request.user)

        instance = self.get_object()

        wishlist.items.remove(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class WishlistByPKViewSet(ModelViewSet):
    queryset = models.Wishlist.objects.all()
    serializer_class = serializers.WishlistByPKSerializer
    # allowed methods
    http_method_names = ['get']

    # def get_object(self, queryset=None, **kwargs):
    #     user = self.kwargs.get('pk')
    #     return get_object_or_404(models.Wishlist, user__username=user)


class AddByLinkViewSet(ModelViewSet):
    serializer_class = serializers.OwnedItemSerializer
    queryset = models.CrawledItem.objects.all()
    permission_classes = [IsAuthenticated]
    # allowed methods
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        try:
            crawled = self.queryset.get(url=self.request.data['url'])
            crawled_serialized = serializers.CrawledItemSerializer(crawled)
        except models.CrawledItem.DoesNotExist:
            return Response({'error': 'The item with this url does not exist in the database.'},
                            status=status.HTTP_400_BAD_REQUEST)
        # save the item to the owned items and all the attributes
        request.data['owner'] = self.request.user.id
        request.data['name'] = crawled_serialized.data['name']
        request.data['season'] = crawled_serialized.data['season']
        request.data['image'] = crawled.image
        request.data['color'] = crawled_serialized.data['color']
        request.data['type'] = crawled_serialized.data['type']
        request.data['material'] = crawled_serialized.data['material']
        request.data['occasion'] = crawled_serialized.data['occasion']
        request.data['brand'] = crawled_serialized.data['brand']

        return super().create(request, *args, **kwargs)


class FilterParamViewSet(ModelViewSet):
    def retrieve(self, request, *args, **kwargs):
        return Response({'error': 'only list allowed'}, status=status.HTTP_400_BAD_REQUEST)


class TypeViewSet(FilterParamViewSet):
    queryset = models.Type.objects.all()
    serializer_class = serializers.TypeSerializer
    # allowed methods
    http_method_names = ['get', 'post']


class BrandViewSet(FilterParamViewSet):
    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandSerializer
    # allowed methods
    http_method_names = ['get', 'post']


class MaterialViewSet(FilterParamViewSet):
    queryset = models.Material.objects.all()
    serializer_class = serializers.MaterialSerializer
    # allowed methods
    http_method_names = ['get', 'post']


class OccasionViewSet(FilterParamViewSet):
    queryset = models.Occasion.objects.all()
    serializer_class = serializers.OccasionSerializer
    # allowed methods
    http_method_names = ['get', 'post']

