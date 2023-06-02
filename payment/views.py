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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Simulate the payment process
        transaction_data = serializer.validated_data
        
        transaction_data['status'] = 'success'  # Update the status to 'success' for testing purposes

        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# class InfoViewSet(ModelViewSet):
#     serializer_class = serializers.InfoSerializer
#     queryset = models.Info.objects.all()
#     http_method_names = ['get', 'post']