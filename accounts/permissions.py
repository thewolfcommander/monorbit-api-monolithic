from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_active and not request.user.is_archived:
            return obj == request.user
        else:
            return False