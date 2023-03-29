from django.db import models
from django.contrib.auth.models import AbstractUser


# create a CustomUser class that has a unique email field
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    phone_number = models.CharField(max_length=15, blank=False, unique=True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    wishlist = models.OneToOneField("Wishlist", on_delete=models.CASCADE, blank=True)


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="ProfilePics/", blank=True)
    theme = models.ForeignKey("Theme", on_delete=models.CASCADE, blank=True)
    background = models.ImageField(upload_to="BackgroundPics/", blank=True)

    def __str__(self):
        return f"{self.user}'s Profile"


class Type(models.Model):
    name = models.CharField(max_length=150, blank=False)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=150, blank=False)

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=150, blank=False)

    def __str__(self):
        return self.name


class Occasion(models.Model):
    name = models.CharField(max_length=150, blank=False)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=150, blank=False)
    season = models.CharField(max_length=150, blank=True)
    image = models.ImageField(upload_to="ItemPics/", Blank=False)
    color = models.CharField(max_length=150, blank=False)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    material = models.ManyToManyField(Material)
    occasion = models.ManyToManyField(Occasion)
    is_owned = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class CrawledItem(Item):
    price = models.IntegerField(blank=False)
    url = models.URLField(blank=False)


class Size(models.Model):
    name = models.CharField(max_length=150, blank=False)

    def __str__(self):
        return self.name


class OwnedItem(Item):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    size = models.ForeignKey("Size", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.owner}'s {self.name}"


class Wishlist(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    items = models.ManyToManyField("CrawledItem", blank=True)

    def __str__(self):
        return f"{self.user}'s Wishlist"


class Theme(models.Model):
    name = models.CharField(max_length=150, blank=False)

    def __str__(self):
        return self.name


class Donations(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(blank=False)

    def __str__(self):
        return f"{self.user} : {self.amount}"
