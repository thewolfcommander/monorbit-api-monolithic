from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to check whether the user who requested have the permission to perform the action
    """

    def has_object_permission(self, request, view, obj):
        """
        Permission to access the detail page
        """
        # Checking if user is active and not archived
        if request.user.is_active and not request.user.is_archived:
            # Validating the user
            return obj == request.user
        else:
            # Cancelling the request for every other condition
            return False