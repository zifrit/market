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
        user_permissions = list(
            request.user.groups.all().values_list("name", flat=True)
        )

        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            obj.creator == request.user
            or "IsAdmin" in user_permissions
            or request.user.is_superuser
        )

    def has_permission(self, request, view):
        user_permissions = list(
            request.user.groups.all().values_list("name", flat=True)
        )

        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser or "IsAdmin" in user_permissions


class IsSuperUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser

    def has_permission(self, request, view):
        return request.user.is_superuser


class CanCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        user_permissions = list(
            request.user.groups.all().values_list("name", flat=True)
        )
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
