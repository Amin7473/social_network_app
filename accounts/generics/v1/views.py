import logging
from rest_framework import views, permissions, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from accounts.generics.v1.serializers import AccountsLoggingSerializer
from accounts.models import AccountsFriendRequestModel, AccountsLoggingModel
from accounts.permissions import IsAdmin
from accounts.users.v1.serializers import AccountsBlockUserSerializer, AccountsPendingFriendRequestSerializer, AccountsSendFriendRequestSerializer, AccountsUnblockUserSerializer, AccountsUpdateFriendRequestSerializer, AccountsUserInfoSerializer
from core.settings import logger
from core.utils.generic_mixins import ResponseMixin
from core.utils.generic_utils import is_filter_required

class AccountsUserActivityLogAPIView(generics.ListAPIView):
    """
    API to retrieve user activity logs.
    """
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = AccountsLoggingSerializer

    def get_queryset(self):
        return AccountsLoggingModel.objects.all().order_by('-created_at')
