from rest_framework import serializers
from . import models
from django.shortcuts import get_object_or_404


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

    class Meta:
        model = models.OwnedItem
        fields = ('id', 'owner', 'name', 'season', 'image', 'color', 'typename', 'type',
                  'material', 'occasion','brand', 'materials', 'occasions', 'is_public', 'score')


class CrawledItemSerializer(ItemSerializer):

    class Meta:
        model = models.CrawledItem
        fields = ('id', 'name', 'season', 'image', 'color', 'typename', 'type',
                  'material', 'occasion','brand', 'materials', 'occasions', 'price', 'url')

# serializer for recommended items
class RecommendedItemSerializer(serializers.ModelSerializer):
    items = CrawledItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.RecommendedItem
        fields = ('id', 'user', 'items')

