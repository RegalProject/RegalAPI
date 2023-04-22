from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404

from . import serializers
from . import models


class ProfileViewSet(ModelViewSet):
    serializer_class = serializers.ProfileSerializer

    # allowed methods
    http_method_names = ['get', 'put', 'patch']

    def get_queryset(self):
        return models.Profile.objects.filter(user=self.request.user)

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(models.Profile, slug=item)
