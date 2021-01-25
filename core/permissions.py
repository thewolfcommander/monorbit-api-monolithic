from rest_framework import permissions

class IsAdmin(permissions.BasePermission):

    message="Only admin can create and update tips"
    def has_permission(self,request,view):
        if request.method=="POST":
            return request.user.is_admin==True
        else:
            return request.user

    def has_object_permission(self,request,view,obj):
        if request.method in ["PUT","PATCH","DELETE"]:
            return request.user.is_admin==True
        
        elif request.method=="GET":
            return request.user

class UserDeviceOwner(permissions.BasePermission):
    message="Only who can update device, who has created."
    def has_object_permission(self,request,view,obj):
        return obj.user == request.user


class NetworkOrderOwner(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        return obj.network.user == request.user
