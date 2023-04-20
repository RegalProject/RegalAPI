from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Type)
admin.site.register(models.Brand)
admin.site.register(models.Material)
admin.site.register(models.Occasion)
admin.site.register(models.Item)
admin.site.register(models.CrawledItem)
admin.site.register(models.OwnedItem)
admin.site.register(models.Wishlist)
admin.site.register(models.RecommendedItem)
