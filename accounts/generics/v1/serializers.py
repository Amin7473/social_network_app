import datetime
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction
from accounts.models import AccountsBlockedUserModel, AccountsFriendRequestModel
from accounts.users.v1.utils.friend_requests import can_send_friend_request, check_rate_limit, get_rejection_cooldown_period
from accounts.models import AccountsLoggingModel

class AccountsLoggingSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source="created_by.username", allow_null=True)
    class Meta:
        model = AccountsLoggingModel
        fields = "__all__"
