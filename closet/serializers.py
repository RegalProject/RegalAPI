from rest_framework import serializers
from . import models

# serializer for items
class OwnedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OwnedItem
        fields = '__all__'