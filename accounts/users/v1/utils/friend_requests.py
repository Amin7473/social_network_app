import datetime
from django.core.cache import cache

from accounts.models import AccountsBlockedUserModel, AccountsFriendRequestModel

def get_rejection_cooldown_period():
        return datetime.timedelta(hours=24)

def rate_limit_key(user_id):
    return f"friend_request_sender_{user_id}"

def check_rate_limit(user):
    key = rate_limit_key(user.id)
    request_count = cache.get(key, 0)
    if request_count >= 3:
        return False
    cache.set(key, request_count + 1, 60)
    return True

def can_send_friend_request(sender, receiver):
    # Checking if sender is blocked by the receiver
    if AccountsBlockedUserModel.objects.filter(blocker=receiver, blocked=sender).exists():
        return False, "You are blocked by this user."

    # Checking if receiver has a pending or cooldown request
    cooldown_request = AccountsFriendRequestModel.objects.filter(
        sender=sender,
        receiver=receiver,
        status='REJECTED',
        rejection_cooldown_date__gt=datetime.datetime.now()
    ).first()
    if cooldown_request:
        return False, "You cannot send a friend request until the cooldown period is over."
    
    return True, None