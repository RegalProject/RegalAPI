from rest_framework import serializers
from . import models


# serializer for items
class ItemSerializer(serializers.ModelSerializer):
    typename = serializers.SerializerMethodField()
    materials = serializers.SerializerMethodField()
    occasions = serializers.SerializerMethodField()

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
        fields = ('id', 'name', 'season', 'image', 'color', 'typename', 'type',
                  'material', 'occasion', 'brand', 'materials', 'occasions')


class OwnedItemSerializer(ItemSerializer):
    owner = serializers.SerializerMethodField()

    def get_owner(self):
        return self.context['user']
    
    class Meta:
        model = models.OwnedItem
        fields = ('id', 'owner', 'name', 'season', 'image', 'color', 'typename', 'type',
                  'material', 'occasion', 'brand', 'materials', 'occasions', 'is_public', 'score')


class CrawledItemSerializer(ItemSerializer):
    class Meta:
        model = models.CrawledItem
        fields = ('id', 'name', 'season', 'image', 'color', 'typename', 'type',
                  'material', 'occasion', 'brand', 'materials', 'occasions', 'price', 'url')


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
    user = serializers.SerializerMethodField()

    @staticmethod
    def get_username(obj):
        return obj.user.username

    def get_user(self):
        return self.context['user']

    class Meta:
        model = models.Wishlist
        fields = ('id', 'user', 'items')


class WishlistByPKSerializer(serializers.ModelSerializer):
    items = CrawledItemSerializer(many=True, read_only=True)

    class Meta:
        model = models.Wishlist
        fields = ('id', 'user', 'items')
