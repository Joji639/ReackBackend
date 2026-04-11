from django.urls import path
from .views import OrderPageView

urlpatterns = [
    path("my-orders/", OrderPageView.as_view()),
]