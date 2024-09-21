from django.contrib import admin
from django.urls import path
from accounts.authentication.v1 import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path(
        "user-registration-api/",
        views.AccountsUserRegistrationAPIView.as_view(),
        name="AccountsUserRegistrationAPIView"
    ),
    path(
        "user-login-api/",
        TokenObtainPairView.as_view(),
        name="TokenObtainPairView"
    ),
    path(
        "user-token-refresh-api/",
        TokenRefreshView.as_view(),
        name="TokenRefreshView"
    ),
]
