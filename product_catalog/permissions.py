from rest_framework import permissions


class IsSubPartOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.network.user == request.user


class IsSubPartDetailOwner(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in ["PUT","PATCH","DELETE"]:
            return obj.network.user == request.user
        elif request.method=="GET":
            return request.user.is_authenticated    



class IsSubSubPartOwner(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        return obj.category.network.user == request.user


class  ProductAdminPermission(permissions.BasePermission):
    """
    If user is admin then they can create network category.
    """
    message="Only admin can create category."
    def has_permission(self,request,view):
        if request.method=="POST":
            return request.user.is_admin==True
        elif request.method=="GET":
            return request.user.is_authenticated


class ProductDetailAdminPermission(permissions.BasePermission):
    """
    If user is admin then they can update network category
    """

    message="Only admin can update network category."
    def has_object_permission(self, request,view,obj):
        if request.method in ["PUT","PATCH","DELETE"]:
            return request.user.is_admin==True
        elif request.method=="GET":
            return request.user.is_authenticated