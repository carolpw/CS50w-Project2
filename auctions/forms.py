from django import forms
from django.forms import ModelForm
from .models import Listing, Comment

# Create the ListingForm class
class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ("title", "description", "price", "image", "category") 

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("text", ) 