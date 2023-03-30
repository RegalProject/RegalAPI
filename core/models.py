from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from django.utils.encoding import force_str


# create a CustomUser class that has a unique email field
# make email the username
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    phone_number = models.CharField(max_length=15, blank=False, unique=True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'email']


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="ProfilePics/", blank=True, null=True)
    theme = models.ForeignKey("Theme", on_delete=models.DO_NOTHING, blank=True, null=True)
    background = models.ImageField(upload_to="BackgroundPics/", blank=True, null=True)
    slug = models.SlugField(blank=True, db_index=True, unique=True)

    @staticmethod
    def get_unique_slug(value):
        slug = slugify(value)
        return slug

    def save(self, *args, **kwargs):
        if not self.slug and self.user:
            self.slug = self.get_unique_slug(force_str(self.user.username))
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user}'s Profile"


class Theme(models.Model):
    name = models.CharField(max_length=150, blank=False)

    def __str__(self):
        return self.name


class Donation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(blank=False)

    def __str__(self):
        return f"{self.user} : {self.amount}"
