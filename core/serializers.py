from rest_framework import serializers
from . import models


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    @staticmethod
    def get_username(obj):
        return obj.user.username

    class Meta:
        model = models.Profile
        fields = ('user', 'username', 'background', 'theme', 'image')


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CustomUser
        fields = ('id',)
