from django.urls import path
from .views import CartListCreateAPIView,CartItemAPIView

urlpatterns = [
    path("cart/",CartListCreateAPIView.as_view()),                  
    path("cart/<int:product_id>/", CartItemAPIView.as_view()), 
]