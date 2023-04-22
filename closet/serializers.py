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


class AddByLinkSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    season = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    material = serializers.SerializerMethodField()
    occasion = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()

    def get_owner(self, obj):
        return self.context['owner']

    def get_name(self, obj):
        return self.context['crawled'].name

    def get_season(self, obj):
        return self.context['crawled'].season

    def get_image(self, obj):
        return self.context['crawled'].image

    def get_color(self, obj):
        return self.context['crawled'].color

    def get_type(self, obj):
        return self.context['crawled'].type

    def get_material(self, obj):
        return self.context['crawled'].material

    def get_occasion(self, obj):
        return self.context['crawled'].occasion

    def get_brand(self, obj):
        return self.context['crawled'].brand

    class Meta:
        model = models.OwnedItem
        fields = ('id', 'name', 'season', 'image', 'color', 'type', 'material',
                  'occasion', 'brand', 'owner', 'is_public', 'score')


class OwnedItemSerializer(ItemSerializer):
    owner = serializers.SerializerMethodField()

    def get_owner(self, obj):
        return self.context['user'].id
    
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
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return self.context['user'].id

    class Meta:
        model = models.Wishlist
        fields = ('id', 'user', 'items')


class WishlistByPKSerializer(serializers.ModelSerializer):
    items = CrawledItemSerializer(many=True, read_only=True)

    class Meta:
        model = models.Wishlist
        fields = ('id', 'user', 'items')
