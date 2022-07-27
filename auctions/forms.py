from django.forms import ModelForm
from  .models import Listing,Bid,Comment,WatchList,Category

class AddListing(ModelForm):
    class Meta:
        model = Listing
        exclude = ['user']

class AddComment(ModelForm):
    class Meta:
        model = Comment
        exclude = ('user','listing')

class AddBid(ModelForm):
    class Meta:
        model = Bid
        exclude = ('user','listing')