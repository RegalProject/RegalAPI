from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from . import serializers
from . import models


class ProfileViewSet(ModelViewSet):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

