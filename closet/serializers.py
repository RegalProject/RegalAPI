from rest_framework import serializers
from django.contrib.auth import get_user_model
from . import models


# serializer for items
class ItemSerializer(serializers.ModelSerializer):
    typename = serializers.SerializerMethodField()
    materials = serializers.SerializerMethodField()
    occasions = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()

    def get_owner(self, obj):
        owner_obj = self.context.get('owner')
        return

    @staticmethod
    def get_typename(obj):
        return obj.type.name

    @staticmethod
    def get_materials(obj):
        return [material.name for material in obj.material.all()]

    @staticmethod
    def get_occasions(obj):
        return [oc.name for oc in obj.occasion.all()]

    class Meta:
        model = models.Item
        fields = ('id', 'name', 'owner', 'season', 'image', 'color', 'typename', 'type',
                  'material', 'occasion', 'brand', 'materials', 'occasions')


class OwnedItemSerializer(ItemSerializer):

    class Meta:
        model = models.OwnedItem
        fields = ItemSerializer.Meta.fields + ('owner', 'is_public', 'score')


class CrawledItemSerializer(ItemSerializer):
    class Meta:
        model = models.CrawledItem
        fields = ItemSerializer.Meta.fields + ('price', 'url')


# serializer for recommended items
class RecommendedItemSerializer(serializers.ModelSerializer):
    items = CrawledItemSerializer(many=True, read_only=True)
    username = serializers.SerializerMethodField()

    @staticmethod
    def get_username(obj):
        return obj.user.username

    class Meta:
        model = models.RecommendedItem
        fields = ('id', 'user', 'username', 'items')


class RecommendedItemByPKSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    @staticmethod
    def get_username(obj):
        return obj.user.username

    class Meta:
        model = models.RecommendedItem
        fields = ('id', 'user', 'username', 'items')


class WishlistSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Wishlist
        fields = ('id', 'user', 'items')


class WishlistByPKSerializer(serializers.ModelSerializer):
    items = CrawledItemSerializer(many=True, read_only=True)

    class Meta:
        model = models.Wishlist
        fields = ('id', 'user', 'items')


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id',)
