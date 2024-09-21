import logging
from rest_framework import views, permissions, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from accounts.models import AccountsFriendRequestModel
from accounts.permissions import IsAdmin, IsReadOnly, IsWriteOnly
from accounts.users.v1.serializers import AccountsBlockUserSerializer, AccountsPendingFriendRequestSerializer, AccountsSendFriendRequestSerializer, AccountsUnblockUserSerializer, AccountsUpdateFriendRequestSerializer, AccountsUserInfoSerializer
from core.settings import logger
from core.utils.generic_mixins import ResponseMixin
from core.utils.generic_utils import is_filter_required


class AccountsUserListAPIView(generics.ListAPIView, ResponseMixin):
    permission_classes = [IsAuthenticated, IsAdmin | IsReadOnly | IsWriteOnly]
    serializer_class = AccountsUserInfoSerializer
    api_logger = logging.LoggerAdapter(
        logger, {"app_name": "AccountsUserListAPIView"}
    )
    queryset = get_user_model().objects.all()
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    """
    API for getting users list
    """

    def get_queryset(self):
        search_param = self.request.query_params.get('search', '').strip()

        if not search_param:
            return get_user_model().objects.all()

        email_filter = Q(email__iexact=search_param)
        name_vector = SearchVector('username',)
        name_query = SearchQuery(search_param)

        queryset = get_user_model().objects.filter(
            email_filter | Q(search_vector=name_vector, search_query=name_query)
        )

        queryset = queryset.annotate(rank=SearchRank(name_vector, name_query)).order_by('-rank')
        return queryset 

    def list(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(
                    self.paginate_queryset(self.get_queryset()), many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            self.api_logger.info(f"AccountsUserListAPIView GET, {str(e)}")
            return self.error_response(data=str(e))


class AccountsFriendRequestAPIView(views.APIView, ResponseMixin):
    permission_classes = [IsAuthenticated, IsAdmin | IsWriteOnly]
    api_logger = logging.LoggerAdapter(
        logger, {"app_name": "AccountsFriendRequestAPIView"}
    )
    """
    POST/PUT Method for sending/accepting/rejecting friend requests
    """
    def post(self, request):
        try:
            data = request.data
            serializer = AccountsSendFriendRequestSerializer(
                data=data,
                context={
                    "logger" : self.api_logger,
                    "request" : request
                    })
            if serializer.is_valid():
                serializer.save()
                return self.success_response(msg="Friend request sent")
            return self.error_response(msg = serializer.errors)
        except Exception as e:
            self.api_logger.info(f"AccountsFriendRequestAPIView POST, {str(e)}")
            return self.error_response(data=str(e))

    def put(self, request):
        try:
            data = request.data
            serializer = AccountsUpdateFriendRequestSerializer(
                data=data,
                context={
                    "logger" : self.api_logger,
                    "request" : request
                    })
            if serializer.is_valid():
                serializer.save()
                return self.success_response(msg=serializer.data["success_msg"])
            return self.error_response(msg = serializer.errors)
        except Exception as e:
            self.api_logger.info(f"AccountsFriendRequestAPIView PUT, {str(e)}")
            return self.error_response(data=str(e))


class AccountsBlockUnblockUserAPIView(views.APIView, ResponseMixin):
    permission_classes = [IsAuthenticated, IsAdmin | IsWriteOnly]
    api_logger = logging.LoggerAdapter(
        logger, {"app_name": "AccountsBlockUnblockUserAPIView"}
    )
    """
    POST/PUT Method for blocking/unblocking users
    """
    def post(self, request):
        try:
            data = request.data
            serializer = AccountsBlockUserSerializer(
                data=data,
                context={
                    "logger" : self.api_logger,
                    "request" : request
                    })
            if serializer.is_valid():
                serializer.save()
                return self.success_response(msg="User blocked successfully")
            return self.error_response(msg = serializer.errors)
        except Exception as e:
            self.api_logger.info(f"AccountsBlockUnblockUserAPIView POST, {str(e)}")
            return self.error_response(data=str(e))

    def put(self, request):
        try:
            data = request.data
            serializer = AccountsUnblockUserSerializer(
                data=data,
                context={
                    "logger" : self.api_logger,
                    "request" : request
                    })
            if serializer.is_valid():
                serializer.save()
                return self.success_response(msg="User removed from block list")
            return self.error_response(msg = serializer.errors)
        except Exception as e:
            self.api_logger.info(f"AccountsBlockUnblockUserAPIView PUT, {str(e)}")
            return self.error_response(data=str(e))


class AccountsFriendsListAPIView(generics.ListAPIView, ResponseMixin):
    permission_classes = [IsAuthenticated, IsAdmin | IsReadOnly | IsWriteOnly]
    serializer_class = AccountsUserInfoSerializer
    api_logger = logging.LoggerAdapter(
        logger, {"app_name": "AccountsFriendsListAPIView"}
    )
    queryset = get_user_model().objects.all()
    """
    API for getting friends list
    """

    def get_cache_key(self, user_id):
        return f"friends_list_{user_id}"

    def get_friends_from_cache(self, user):
        key = self.get_cache_key(user.id)
        return cache.get(key)

    def cache_friends_list(self, user, friends_list):
        key = self.get_cache_key(user.id)
        # Caching the friends list for 2 minutes
        cache.set(key, friends_list, 120)

    def get_queryset(self):
        user = self.request.user

        cached_friends = self.get_friends_from_cache(user)
        if cached_friends:
            return cached_friends
        
        friends = AccountsFriendRequestModel.objects.filter(
            Q(sender=user, status='ACCEPTED') | Q(receiver=user, status='ACCEPTED')
        ).select_related('sender', 'receiver')

        queryset = [f.sender if f.receiver == user else f.receiver for f in friends]

        # Caching the friends list
        self.cache_friends_list(user, queryset)

        return queryset

    def list(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(
                    self.paginate_queryset(self.get_queryset()), many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            self.api_logger.info(f"AccountsFriendsListAPIView GET, {str(e)}")
            return self.error_response(data=str(e))


class AccountsPendingFriendRequestsAPIView(generics.ListAPIView, ResponseMixin):
    permission_classes = [IsAuthenticated, IsAdmin | IsReadOnly | IsWriteOnly]
    serializer_class = AccountsPendingFriendRequestSerializer
    api_logger = logging.LoggerAdapter(
        logger, {"app_name": "AccountsPendingFriendRequestsAPIView"}
    )
    queryset = AccountsFriendRequestModel.objects.all()
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    """
    API for getting pending friend requests
    """

    def get_queryset(self):
        user = self.request.user
        queryset = AccountsFriendRequestModel.objects.filter(receiver=user, status='PENDING').order_by('-created_at')
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(
                    self.paginate_queryset(self.get_queryset()), many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            self.api_logger.info(f"AccountsPendingFriendRequestsAPIView GET, {str(e)}")
            return self.error_response(data=str(e))
