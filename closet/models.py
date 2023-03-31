from django.db import models
from django.conf import settings


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
    image = models.ImageField(upload_to="ItemPics/", blank=False)
    color = models.CharField(max_length=150, blank=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    material = models.ManyToManyField(Material)
    occasion = models.ManyToManyField(Occasion)

    def __str__(self):
        return self.name


class CrawledItem(Item):
    price = models.IntegerField(blank=False)
    url = models.URLField(blank=False)


class OwnedItem(Item):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.owner}'s {self.name}"


class Wishlist(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField("CrawledItem", blank=True)

    def __str__(self):
        return f"{self.user}'s Wishlist"


class RecommendedItem(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField("CrawledItem", blank=True)

    def __str__(self):
        return f"{self.user}'s Recommended items"
