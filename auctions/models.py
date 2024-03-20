from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.name

class Listing(models.Model):
    title = models.CharField(max_length=32)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    description = models.CharField(max_length=256)
    price = models.FloatField()
    date =  models.DateField(auto_now=True)
    image = models.CharField(max_length=256, blank=True) #ImageField, install Pillow?
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category", blank=True)
    active = models.BooleanField(default=True)

class Bids(models.Model):
    pass

class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    text = models.CharField(max_length=256)

