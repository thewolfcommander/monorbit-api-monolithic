from rest_framework import permissions

class JobProfilePermission(permissions.BasePermission):
    """
    Only job profile owner can update their profile.
    """
    message="Only job profile owner can update their profile."
    def has_object_permission(self,request,view,obj):
        if request.method in ["PUT","PATCH","DELETE"]:
            return obj.user == request.usr