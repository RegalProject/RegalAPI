from rest_framework import serializers
from . import models
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def create(self, validated_data):
        super().create(validated_data)

    def update(self, instance, validated_data):
        super().update(instance, validated_data)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['phone'] = user.phone_number
        token['email'] = user.email
        profile_data = ProfileSerializer(user.profile).data
        token['profile_photo'] = f'{profile_data["image"]}'
        token['background'] = f'{profile_data["background"]}'

        return token


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
