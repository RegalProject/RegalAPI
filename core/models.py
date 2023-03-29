from django.db import models
from django.contrib.auth.models import AbstractUser


# create a CustomUser class that has an unique email field
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    phone_number = models.CharField(max_length=15, blank=False, unique=True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
