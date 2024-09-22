from django.contrib import admin
from django.urls import path
from accounts.generics.v1 import views

urlpatterns = [
    path(
        "log-list-api/",
        views.AccountsUserActivityLogAPIView.as_view(),
        name="AccountsUserActivityLogAPIView"
    )
]
