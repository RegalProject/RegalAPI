from rest_framework import serializers
from . import models

class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    
    class Meta:
        model = models.Profile
        fields = ('id', 'user_id', 'background', 'theme', 'image')