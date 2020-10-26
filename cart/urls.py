from django.urls import path

from .views import *

app_name='cart'

urlpatterns = [
    path('create/', CreateCart.as_view(), name='create'),
    path('all/', ListCart.as_view(), name='all'),
    path('detail/<slug:id>/', UpdateCart.as_view(), name='detail'),
    
    path('entry/product/create/', CreateProductEntry.as_view(), name='product_entry_create'),
    path('entry/product/all/', ListProductEntry.as_view(), name='product_entry_all'),
    path('entry/product/detail/<int:id>/', UpdateProductEntry.as_view(), name='product_entry_detail'),

    # Wishlist
    path('wishlist/', GetOrCreateWishlist.as_view(), name='get_or_create_wishlist'),
    path('wishlist/detail/<slug:id>/', ShowWishlistDetail.as_view(), name='wishlist_detail'),
    path('wishlist/product/create/', AddWishlistProductEntry.as_view(), name='create_wishlist_entry'),
    path('wishlist/product/delete/<slug:id>/', DeleteWishlistProductEntry.as_view(), name='delete_wishlist_entry'),
]