from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    pass


class Category(models.Model):
    category_name = models.CharField(max_length=600)
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.category_name}'


class Listing(models.Model):
    listing_image = models.ImageField(
        upload_to='listing/%Y/%m/%d/', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, 
            on_delete=models.CASCADE) 

    listing_name = models.CharField(max_length=600)
    listing_bid = models.DecimalField(max_digits=7, decimal_places=2)
    is_listing_active = models.BooleanField(default=False)
    listing_detail = models.TextField(max_length=900)
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.listing_name} is active-{self.is_listing_active}'


class Comment(models.Model):
    user = models.ForeignKey(User,
        on_delete = models.CASCADE)
    listing = models.ForeignKey(Listing, 
        on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=600)
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'comment for {self.listing.listing_name} time{self.pub_date}'


class Bid(models.Model):
    user =  models.ForeignKey(User,
        on_delete = models.CASCADE)
    listing = models.ForeignKey(Listing, 
        on_delete=models.CASCADE)
    bid = models.DecimalField('place your bid',max_digits=7, 
        decimal_places=2)
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.bid}'


class WatchList(models.Model):
    user = models.ForeignKey(User,
        on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, 
        on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now=True)
    