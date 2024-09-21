from django.contrib import admin
from django.urls import path
from accounts.users.v1 import views

urlpatterns = [
    path(
        "user-list-api/",
        views.AccountsUserListAPIView.as_view(),
        name="AccountsUserListAPIView"
    ),
    path(
        "friend-request-api/",
        views.AccountsFriendRequestAPIView.as_view(),
        name="AccountsFriendRequestAPIView"
    ),
    path(
        "user-block-unblock-api/",
        views.AccountsBlockUnblockUserAPIView.as_view(),
        name="AccountsBlockUnblockUserAPIView"
    ),
    path(
        "friends-list-api/",
        views.AccountsFriendsListAPIView.as_view(),
        name="AccountsFriendsListAPIView"
    ),
    path(
        "pending-friends-requests-api/",
        views.AccountsFriendsListAPIView.as_view(),
        name="AccountsFriendsListAPIView"
    )
]
