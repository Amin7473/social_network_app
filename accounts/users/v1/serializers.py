import datetime
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction
from accounts.models import AccountsBlockedUserModel, AccountsFriendRequestModel
from accounts.users.v1.utils.friend_requests import can_send_friend_request, check_rate_limit, get_rejection_cooldown_period
from core.utils.generic_utils import create_log

class AccountsUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ["password"]


class AccountsSendFriendRequestSerializer(serializers.Serializer):
    reciever_id = serializers.CharField(required=True)

    def validate(self, attrs):
        request = self.context["request"]
        sender = request.user
        receiver = get_user_model().objects.get(id=attrs["receiver_id"])

        if not check_rate_limit(sender):
            raise serializers.ValidationError("Limit exceeded. You can only send 3 friend requests per minute.")

        can_send, error_message = can_send_friend_request(sender, receiver)
        if not can_send:
            raise serializers.ValidationError(error_message)
        return attrs

    def create(self, validated_data):
        request = self.context["request"]
        sender = request.user
        receiver = get_user_model().objects.get(id=validated_data["receiver_id"])
        with transaction.atomic():
            friend_request, created = AccountsFriendRequestModel.objects.get_or_create(sender=sender, receiver=receiver)
            if not created and friend_request.status == 'REJECTED':
                # Reseting cooldown period for rejected request
                friend_request.status = 'PENDING'
                friend_request.rejection_cooldown_date = None
                friend_request.save(update_fields=['status', 'rejection_cooldown_date'])
            create_log(
                msg=f"Friend request sent - Sender : {sender.username} - Reciever : {receiver.username}",
                user=request.user
            )
        return validated_data

class AccountsUpdateFriendRequestSerializer(serializers.Serializer):
    request_id = serializers.CharField(required=True)
    status = serializers.CharField(required=True)
    success_msg = serializers.CharField(required=False)

    def validate(self, attrs):
        user = self.context["request"].user
        try:
            _ = AccountsFriendRequestModel.objects.get(id=attrs["request_id"], receiver=user)
        except AccountsFriendRequestModel.DoesNotExist:
            raise serializers.ValidationError("Friend request not found")
        return attrs

    def create(self, validated_data):
        request = self.context["request"]
        status = validated_data["status"]
        friend_request = AccountsFriendRequestModel.objects.get(id=validated_data["request_id"])
        validated_data["success_msg"] = "Success"
        with transaction.atomic():
            if status == "ACCEPTED":
                friend_request.status = 'ACCEPTED'
                friend_request.save(update_fields=['status'])
                validated_data["success_msg"] = "Friend request accepted"
                create_log(
                    msg=f"Friend request accepted - Sender : {friend_request.sender.username} - Reciever : {friend_request.receiver.username}",
                    user=request.user
                )
            elif status == "REJECTED":
                friend_request.status = 'REJECTED'
                friend_request.rejection_cooldown_date = datetime.datetime().now() + get_rejection_cooldown_period()
                friend_request.save(update_fields=['status', 'rejection_cooldown_date'])
                validated_data["success_msg"] = "Friend request rejected"
                create_log(
                    msg=f"Friend request rejected - Sender : {friend_request.sender.username} - Reciever : {friend_request.receiver.username}",
                    user=request.user
                )
        return validated_data


class AccountsBlockUserSerializer(serializers.Serializer):
    block_user_id = serializers.CharField(required=True)

    def validate(self, attrs):
        try:
            _ = get_user_model().objects.get(id = attrs["block_user_id"])
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError("User not found")
        return attrs

    def create(self, validated_data):
        request = self.context["request"]
        with transaction.atomic():
            blocker = request.user
            blocked = get_user_model().objects.get(id=validated_data["block_user_id"])

            AccountsBlockedUserModel.objects.get_or_create(blocker=blocker, blocked=blocked)
            create_log(
                msg=f"User blocked - Blocker : {blocker.username} - Blocked : {blocked.username}",
                user=request.user
            )
        return validated_data


class AccountsUnblockUserSerializer(serializers.Serializer):
    unblock_user_id = serializers.CharField(required=True)

    def validate(self, attrs):
        try:
            _ = get_user_model().objects.get(id = attrs["unblock_user_id"])
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError("User not found")
        return attrs

    def create(self, validated_data):
        request = self.context["request"]
        with transaction.atomic():
            blocker = request.user
            blocked = get_user_model().objects.get(id=validated_data["unblock_user_id"])
            AccountsBlockedUserModel.objects.filter(blocker=blocker, blocked=blocked).delete()
            create_log(
                msg=f"User Unblocked - Blocker : {blocker.username} - Blocked : {blocked.username}",
                user=request.user
            )
        return validated_data


class AccountsSudoUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email']

class AccountsPendingFriendRequestSerializer(serializers.ModelSerializer):
    sender = AccountsSudoUserInfoSerializer(read_only=True)

    class Meta:
        model = AccountsFriendRequestModel
        fields = ['id', 'sender', 'created_at']

