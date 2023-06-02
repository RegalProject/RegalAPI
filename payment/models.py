from django.db import models
from django.conf import settings

class Transaction(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    )

    name = models.CharField(max_length=100, default='')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    # Other fields you may need for your transaction

    def __str__(self):
        return f"Transaction #{self.pk}: {self.amount} ({self.status})"
    
# class Info(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)