from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from rest_framework_simplejwt.views import TokenObtainPairView

from . import serializers
from . import models


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer


class ProfileViewSet(ModelViewSet):
    serializer_class = serializers.ProfileSerializer

    http_method_names = ['get', 'put']

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



class UserListView(ModelViewSet):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.CustomUserSerializer

    http_method_names = ['get']

    def get_object(self):
        return Response({'error': 'only list request allowed'}, status=status.HTTP_400_BAD_REQUEST)
