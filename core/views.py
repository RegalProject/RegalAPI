from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from . import serializers
from . import models


class ProfileViewSet(ModelViewSet):
    serializer_class = serializers.ProfileSerializer

    http_method_names = ['get', 'patch']

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Profile.objects.filter(user=self.request.user)

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(models.Profile, slug=item)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"user": self.request.user})
        return context

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = models.Profile.objects.get(user=self.request.user)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class UserListView(ModelViewSet):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.CustomUserSerializer

    http_method_names = ['get']

    def get_object(self):
        return Response({'error': 'only list request allowed'}, status=status.HTTP_400_BAD_REQUEST)
