from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from . import models
from . import serializers
from rest_framework import status


class TransactionViewSet(ModelViewSet):
    serializer_class = serializers.TransactionSerializer
    queryset = models.Transaction.objects.all()
    http_method_names = ['post']

    

# class InfoViewSet(ModelViewSet):
#     serializer_class = serializers.InfoSerializer
#     queryset = models.Info.objects.all()
#     http_method_names = ['get', 'post']