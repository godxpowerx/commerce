from django.contrib import admin

from .models import Category,User, Listing,WatchList,Bid

admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(WatchList)
admin.site.register(User)
admin.site.register(Bid)
