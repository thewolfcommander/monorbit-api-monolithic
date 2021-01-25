from rest_framework import permissions

class IsCartOwner(permissions.BasePermission):
    """
    Updating cart. Only cart owner can update.
    """
    message="Only cart owner can update."
    def has_object_permission(self,request,view,obj):
        return obj.user == request.user

class IsCartProductOwner(permissions.BasePermission):
    """
    Permissions for ProductEntry. Only Cart Owner who has created cart can update their cart product.
    """

    message="only cart owner user can update cart."
    def has_object_permission(self,request,view,obj):
        return obj.cart.user==request.user

class AddWishlistPermission(permissions.BasePermission):

    message="The owner of cart who add product in wishlist can delete."
    def has_object_permission(self,request,view,obj):
        return obj.wishlist.user == request.user


class ProductOrderStatus(permissions.BasePermission):
    """
    Permission for order status that only product owner(network owner) or admin can change.
    """

    message="Only Product owner who has network or Admin can update product status."
    def has_object_permission(self,request,view,obj):
        return obj.product.network.user == request.user or request.user.is_admin == True 