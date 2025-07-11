from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Является ли пользователь владельцем"""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
