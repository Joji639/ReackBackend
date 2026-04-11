from django.urls import path
from .views import *

urlpatterns = [


    path("users/", AdminUserListView.as_view()),
    path("users/<int:pk>/toggle-status/", ToggleUserStatusView.as_view()),
    path("users/<int:pk>/delete/", DeleteUserView.as_view()),


    path("products/", AdminProductListCreateView.as_view()),
    path("products/<int:pk>/", AdminProductDetailView.as_view()),


    path("orders/", AdminOrderListView.as_view()),
    path("orders/<int:pk>/status/", UpdateOrderStatusView.as_view()),


    path("dashboard/", AdminDashboardView.as_view()),
]