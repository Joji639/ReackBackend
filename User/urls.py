from django.urls import path
from .views import SignUpView, LoginView,LogoutView,ForgotPasswordView,ResetPasswordView

urlpatterns = [
    path("signup/", SignUpView.as_view()),
    path("login/", LoginView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('forgot-password/',ForgotPasswordView.as_view()),
    path('reset-password/',ResetPasswordView.as_view()),
]