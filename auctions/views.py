from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout,get_user
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from httplib2 import Http

from .models import Category, User,Listing,WatchList,Bid
from .forms import AddListing,AddBid,AddComment
from .utils import valid_bid

@require_http_methods(['GET', 'POST'])
def index(request):
    listing_list = Listing.objects.filter(is_listing_active=True)
    return render(request, "auctions/index.html",
    {'listing':listing_list})


@require_http_methods(['POST'])
@login_required(login_url='auctions:login')
def add_comment(request, product_id):
    form = AddComment(request.POST)
    if form.is_valid():
        listing = Listing.objects.get(pk=product_id)
        new_comment = form.save(commit=False)
        new_comment.user = request.user
        new_comment.listing = listing
        new_comment.save()
    return HttpResponseRedirect(reverse('auctions:product_page' ,args=[product_id,]))


@require_http_methods(['GET', 'POST'])
@login_required(login_url='auctions:login')
def watchlist(request):
    watch_list = WatchList.objects.filter(user=get_user(request))
    return render(request, 'auctions/watchlist.html',{
        'watch_list': watch_list
    }) 


@require_http_methods(['GET', 'POST'])
@login_required(login_url='auctions:login')
def add_watchlist(request,product_id):
    listing = Listing.objects.get(pk=product_id)
    watch = WatchList.objects.filter(listing=listing)
    if not watch:
        watch_list = WatchList(user=get_user(request),
                    listing=listing)
        watch_list.save()
    return HttpResponseRedirect(reverse('auctions:product_page',
    args=[product_id]))


@require_http_methods(['GET', 'POST'])
@login_required(login_url='auctions:login')
def remove_watchlist(request, watch_id):
    listing = WatchList.objects.get(pk=watch_id)
    listing.delete()
    return HttpResponseRedirect(reverse('auctions:watchlist'))


@require_http_methods(['GET', 'POST'])
@login_required(login_url='auctions:login')
def close_listing(request,product_id):
    listing = Listing.objects.get(pk=product_id)
    listing.is_listing_active = False
    listing.save()
    return HttpResponseRedirect(reverse('auctions:product_page',
                                        args=[product_id]))


@require_http_methods(['GET', 'POST'])
def product_page(request,product_id):
    context={}
    listing = Listing.objects.filter(pk=product_id)
    try:
        high_bid = Bid.objects.filter(listing=listing[0]).order_by('bid')[0]
        context['high_bid'] = high_bid
    except:
        pass

    bidform = AddBid()
    commentform = AddComment()
    context.update({'listing': listing, 'bidform': bidform, 'commentform': commentform,
               })
    return render(request, 'auctions/product_page.html',
    context
    )

def get_category(request,cat_id):
    category = Category.objects.get(pk=cat_id)
    listing = Listing.objects.filter(category=category)
    return render(request, "auctions/index.html",
                  {'listing': listing})


@require_http_methods(['GET', 'POST'])
@login_required(login_url='auctions:login')
def addbid(request, product_id):
    bidform = AddBid(request.POST)
    if bidform.is_valid():
        listing = Listing.objects.get(pk=product_id)
        if listing.is_listing_active:
            bids = listing.bid_set.all()
            current_bid = request.POST['bid']
            if valid_bid(bids,current_bid) and listing.listing_bid <= int(current_bid):
                bidform = bidform.save(commit=False)
                bidform.user = get_user(request)
                bidform.listing = listing
                bidform.save()
    return HttpResponseRedirect(reverse('auctions:product_page',args=[product_id]))


@require_http_methods(['GET','POST'])
@login_required(login_url='auctions:login')
def addlisting(request):
    form = AddListing(request.POST,request.FILES)
    if request.method == 'POST':
        form = AddListing(request.POST,request.FILES)
        if form.is_valid():
            listing_new = form.save(commit=False)
            listing_new.user = get_user(request)
            listing_new.save()
            return HttpResponseRedirect(reverse('auctions:index'))
    
    return render(request, 'auctions/addlisting.html',
        {'form':form})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")
