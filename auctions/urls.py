from django.urls import path

from . import views

app_name = 'auctions'

urlpatterns = [
    path("", views.index, name="index"),
    path('addlisting',views.addlisting,name='addlisting'),
    path('product_page/<int:product_id>',views.product_page,name='product_page'),
    path('comment/<int:product_id>',views.add_comment,name='comment'),
    path('watchlist',views.watchlist,name='watchlist'),
    path('addwatchlist/<int:product_id>', views.add_watchlist,name='addwatchlist'),
    path('addbid/<int:product_id>',views.addbid,name='addbid'),
    path('get_category/<int:cat_id>',views.get_category,name='get_category'),
    path('removewatch/<int:watch_id>',views.remove_watchlist, name='removewatch'),
    path('closelisting/<int:product_id>',views.close_listing,name='closelisting'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
