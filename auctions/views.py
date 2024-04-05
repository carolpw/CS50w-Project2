from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, Category, Bid
from .forms import ListingForm, CommentForm
from django.contrib.auth.decorators import login_required


def index(request):
    activeListings = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "active_listings": activeListings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the listing
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()

            # Create a bid with the starting bid entered in the form
            starting_bid = form.cleaned_data['starting_bid']
            bid = Bid(user=request.user, amount=starting_bid, listing=listing)
            bid.save()
            
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('index')) #INDEX? MAYBE CHANGE. I couldn't do it with 'auctions:index'

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ListingForm()

    return render(request, 'auctions/createListing.html', {'form': form})


def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    current_price = listing.bids.order_by('-amount').first().amount if listing.bids.exists() else 0
    in_watchlist = True
    form = None

    #Comment section
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                form.instance.author = request.user
                form.instance.listing = listing
                form.save()
                # Redirect to the same page after adding comment
                return HttpResponseRedirect(reverse('listing', args=(listing_id, )))
        else:
            form = CommentForm()


    return render(request, "auctions/listing.html", {
        "listing": listing,
        "current_price": current_price,
        "in_watchlist": in_watchlist,
        "form": form
    })

def category_listing(request, category_id):
    listings_cat = Listing.objects.filter(active=True, category=category_id)
    category = Category.objects.get(pk=category_id)
    return render(request, "auctions/category.html", { 
        "listings_cat": listings_cat,
        "category": category
    })

@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "watchlist": request.user.watchlist.all()
    })

@login_required
def watch(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    request.user.watchlist.add(listing)
    request.user.save()
    return HttpResponseRedirect(reverse('watchlist'))
    
@login_required
def unwatch(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    request.user.watchlist.remove(listing)
    request.user.save()
    return HttpResponseRedirect(reverse('index'))

