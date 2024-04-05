from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True, null=True, related_name="watchlist")
    pass

class Category(models.Model):
    name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.name
    
 



class Listing(models.Model):
    title = models.CharField(max_length=32)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing")
    description = models.CharField(max_length=256)
    date = models.DateField(auto_now=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category", blank=True)
    active = models.BooleanField(default=True)


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.FloatField(default=0)
    date = models.DateTimeField(auto_now=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")



class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    date_added = models.DateTimeField(default=timezone.now, editable=False)

def __str__(self):
    return f"Comment by {self.author.username} on {self.listing.title}"


