from rest_framework.permissions import BasePermission

class IsReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'READ'

class IsWriteOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'WRITE'

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'ADMIN'
