from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartDetailView.as_view(), name='detail'),
    path('add/', views.add_to_cart, name='add'),
    path('remove/', views.remove_from_cart, name='remove'),
    path('update/', views.update_cart_item, name='update'),
    path('clear/', views.clear_cart, name='clear'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('checkout/success/', views.checkout_success, name='checkout_success'),
    
    # Wishlist URLs
    path('wishlist/', views.WishListView.as_view(), name='wishlist'),
    path('wishlist/add/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/', views.remove_from_wishlist, name='remove_from_wishlist'),
]