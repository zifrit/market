from rest_framework import permissions
from rest_framework import generics
import logging

from rest_framework.permissions import IsAuthenticated

admin_log = logging.getLogger("admin")


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.creator == request.user


class IsOwnerOrIsAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            obj.creator == request.user
            or "IsAdmin" in request.user_groups_name
            or request.user.is_superuser
        )

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser or "IsAdmin" in request.user_groups_name


class IsSuperUserOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser and "IsAdmin" in request.user_groups_name

    def has_permission(self, request, view):
        return request.user.is_superuser and "IsAdmin" in request.user_groups_name


class CanCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        user_permissions = request.user_groups_name
        return (
            "IsAdmin" in user_permissions
            or "IsOwner" in user_permissions
            or request.user.is_superuser
        )


class CustomBasePermission(generics.GenericAPIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), CanCreate()]
        return [IsAuthenticated(), IsOwnerOrIsAdminOrReadOnly()]
