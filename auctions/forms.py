from django import forms
from django.forms import ModelForm
from .models import Listing, Comment

# Create the ListingForm class
class ListingForm(forms.ModelForm):
    starting_bid = forms.FloatField(label='Starting Bid')

    class Meta:
        model = Listing
        fields = ("title", "description", "image", "category")

    def clean_starting_bid(self):
        starting_bid = self.cleaned_data['starting_bid']
        if starting_bid <= 0:
            raise forms.ValidationError("Starting bid must be greater than zero.")
        return starting_bid

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("text", ) 