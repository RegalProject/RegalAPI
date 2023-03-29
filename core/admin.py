from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.CustomUser)
admin.site.register(models.Profile)
admin.site.register(models.Theme)
admin.site.register(models.Donation)