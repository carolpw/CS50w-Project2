from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.create_listing, name="create_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    #path("categories", views.categories, name="categories"),
    path("<int:listing_id>", views.listing, name="listing"),
    #path("category", views.category, name="category"), # change to name of the category 
    path('category/', views.categories, name='category'),
    path('category/<int:category_id>/', views.category_listing, name='category_listing')
]
