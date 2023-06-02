from rest_framework import serializers
from . import models

class TransactionSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=models.Transaction.STATUS_CHOICES, default='pending', read_only=True)
    
    class Meta:
        model = models.Transaction
        fields = ('id', 'name', 'amount', 'status', 'created_at')

# class InfoSerializer(serializers.Serializer):
#     class Meta:
#         model = models.Info
#         fields = ('id', 'user', 'amount')