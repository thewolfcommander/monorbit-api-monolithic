from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

    
class IsSubPartOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.network.user == request.user

class IsSubSubPartOwner(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        return obj.job.network == request.user


class  NetworkAdminPermission(permissions.BasePermission):
    """
    If user is admin then they can create network category.
    """
    message="Only admin can create category."
    def has_permission(self,request,view):
        if request.method=="POST":
            return request.user.is_admin==True
        elif request.method=="GET":
            return request.user.is_authenticated

class NetworkDetailAdminPermission(permissions.BasePermission):
    """
    If user is admin then they can update network category
    """

    message="Only admin can update network category."
    def has_object_permission(self, request,view,obj):
        if request.method in ["PUT","PATCH","DELETE"]:
            return request.user.is_admin==True
        elif request.method=="GET":
            return request.user.is_authenticated    



