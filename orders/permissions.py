from rest_framework import permissions

class IsOwnerOfCart(permissions.BasePermission):
    message="Only of cart can view their order and update it."
    def has_object_permission(self,request,view,obj):
        return obj.cart.user == request.user