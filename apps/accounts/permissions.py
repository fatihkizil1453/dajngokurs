# apps/accounts/permissions.py
from rest_framework import permissions

class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'SELLER')

class IsBuyer(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'BUYER')

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute, or check implementation in view.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Check diverse owner fields commonly used
        return (getattr(obj, 'user', None) == request.user) or \
               (getattr(obj, 'owner', None) == request.user) or \
               (getattr(obj, 'seller', None) == request.user) or \
               (getattr(obj, 'buyer', None) == request.user) or \
               (getattr(obj, 'author', None) == request.user)
