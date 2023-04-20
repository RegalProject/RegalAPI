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
        mats = []
        for material in obj.material.all():
            mats.append(material.name)
        return mats

    @staticmethod
    def get_occasions(obj):
        occasions = []
        for oc in obj.occasion.all():
            occasions.append(oc.name)
        return occasions

    class Meta:
        model = models.Item
        fields = ('id', 'name', 'season', 'image', 'color', 'typename',
                  'brand', 'materials', 'occasions')


class OwnedItemSerializer(ItemSerializer):

    class Meta:
        model = models.OwnedItem
        fields = ('id', 'name', 'season', 'image', 'color', 'typename',
                  'brand', 'materials', 'occasions', 'is_public', 'score')


class CrawledItemSerializer(ItemSerializer):

    class Meta:
        model = models.CrawledItem
        fields = ('id', 'name', 'season', 'image', 'color', 'typename',
                  'brand', 'materials', 'occasions', 'price', 'url')
