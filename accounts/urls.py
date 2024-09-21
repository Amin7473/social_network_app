from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("api/authentication/v1/", include("accounts.authentication.v1.urls")),
    path("api/users/v1/", include("accounts.users.v1.urls")),
    path("api/generics/v1/", include("accounts.generics.v1.urls")),
]
