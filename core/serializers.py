from rest_framework import serializers
from . import models


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_user(self):
        return self.context['user']

    @staticmethod
    def get_username(obj):
        return obj.user.username
    

    class Meta:
        model = models.Profile
        fields = ('user', 'username', 'background', 'theme', 'image')
