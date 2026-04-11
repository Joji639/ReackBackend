from django.urls import path
from .views import WishlistAPIView,WishlistDetailAPIView

urlpatterns = [
    path("wishlist/", WishlistAPIView.as_view()),                  
    path("wishlist/<int:product_id>/", WishlistDetailAPIView.as_view()), 
]