from django.db import models
from django.contrib.auth.models import AbstractUser


# create a CustomUser class that has a unique email field
# make email the username
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    phone_number = models.CharField(max_length=15, blank=False, unique=True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="ProfilePics/", blank=True)
    theme = models.ForeignKey("Theme", on_delete=models.DO_NOTHING, blank=True)
    background = models.ImageField(upload_to="BackgroundPics/", blank=True)

    def __str__(self):
        return f"{self.user}'s Profile"


class Theme(models.Model):
    name = models.CharField(max_length=150, blank=False)

    def __str__(self):
        return self.name


class Donations(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(blank=False)

    def __str__(self):
        return f"{self.user} : {self.amount}"
