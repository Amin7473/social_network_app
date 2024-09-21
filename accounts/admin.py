from django.contrib import admin
from django.utils.html import format_html
from .models import (
    UserModel, 
    AccountsLoggingModel, 
    AccountsFriendRequestModel, 
    AccountsBlockedUserModel
)

@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'phone_number', 'role', 'is_active', 'is_verified', 'is_superuser')
    list_filter = ('is_active', 'is_verified', 'is_superuser', 'role')
    search_fields = ('email', 'username', 'phone_number')

@admin.register(AccountsLoggingModel)
class AccountsLoggingModelAdmin(admin.ModelAdmin):
    list_display = ('message', 'created_by', 'created_at')
    search_fields = ('message',)
    list_filter = ('created_by',)

@admin.register(AccountsFriendRequestModel)
class AccountsFriendRequestModelAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'status', 'rejection_cooldown_date')
    list_filter = ('status',)
    search_fields = ('sender__email', 'receiver__email')

@admin.register(AccountsBlockedUserModel)
class AccountsBlockedUserModelAdmin(admin.ModelAdmin):
    list_display = ('blocker', 'blocked')
    search_fields = ('blocker__email', 'blocked__email')
    list_filter = ('blocker', 'blocked')