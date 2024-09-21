from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.contrib.auth import get_user_model
from accounts.managers import CustomUserManager
from core.utils.enums import FriendRequestStatusEnums, UserRoleEnums
from core.utils.generic_models import CoreGenericModel


class UserModel(AbstractBaseUser, PermissionsMixin, CoreGenericModel):
    username = models.CharField(max_length=100, null=True, blank=True, unique=True, db_index=True)
    email = models.EmailField(blank=True, max_length=255, null=True, unique=True, db_index=True)
    country_code = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    role = models.CharField(max_length=10,
        choices=UserRoleEnums.choices(),
        null=False,
        blank=True)
    timezone_info = models.CharField(max_length=50, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    class Meta:
        db_table = "USERS"
        indexes = [
            models.Index(fields=['email'], name='email_idx'),
            models.Index(fields=['username'], name='username_idx'),
        ]

    def __str__(self):
        return str(self.email)


class AccountsLoggingModel(CoreGenericModel):
    message = models.TextField()
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='AccountsLoggingModel_created_by',
        null=True,
        blank=True
    )

class AccountsFriendRequestModel(CoreGenericModel):
    sender = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='AccountsFriendRequestModel_sender'
    )
    receiver = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='AccountsFriendRequestModel_receiver'
    )
    status = models.CharField(
        max_length=15,
        choices=FriendRequestStatusEnums.choices(),
        default='PENDING'
    )
    rejection_cooldown_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('sender', 'receiver')


class AccountsBlockedUserModel(CoreGenericModel):
    blocker = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='AccountsBlockedUserModel_blocker'
    )
    blocked = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='AccountsBlockedUserModel_blocked'
    )

    class Meta:
        unique_together = ('blocker', 'blocked')
