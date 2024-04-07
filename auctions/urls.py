from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.create_listing, name="create_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("category/", views.categories, name="category"),
    path("category/<int:category_id>/", views.category_listing, name="category_listing"),
    path("watch/<int:listing_id>", views.watch, name="watch"),
    path("unwatch/<int:listing_id>", views.unwatch, name="unwatch"),
    path("bid/<int:listing_id>", views.place_bid, name="place_bid"),
    path("close_auction/<int:listing_id>", views.close_auction, name="close_auction")
]
