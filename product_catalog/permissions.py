from rest_framework import permissions
from .models import ProductImage,Product


class IsSubPartOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.network.user == request.user


class IsSubPartDetailOwner(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in ["PUT","PATCH","DELETE"]:
            return obj.network.user == request.user
        elif request.method=="GET":
            return request.user.is_authenticated    

class IsProductOwnersVariant(permissions.BasePermission):
    """
    Permission for Image, Video, Tag, Size, color, Specification and Extra of Product. 
    If Product's User is request user then they create these otherwise not.
    """

    message="If Product user is requested user then only variant(image,video,document,tag) will create."
    def has_permission(self,request,view):
        product_id = request.data["product"]
        print(product_id)
        product = Product.objects.get(id=product_id)
        return product.network.user == request.user

     

class IsProductOwnersVariantDetail(permissions.BasePermission):
    """
    Permission for Image, Video, Tag, Size, color, Specification and Extra of Product. 
    If Product's User is request user then they update these otherwise not.
    """
    message="You are not owner of this object."
    def has_object_permission(self,request,view,obj):
        if request.method in ["PUT","PATCH","DELETE"]:
            return obj.product.network.user == request.user
        elif request.method=="GET":
            return request.user.is_authenticated


class IsSubSubPartOwner(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        return obj.category.network.user == request.user

class IsReviewOwner(permissions.BasePermission):
    """
    Review Owner can update and delete the review.
    """

    message="Only review owner can update review"
    def has_object_permission(self,request,view,obj):
        if request.method in ["PUT","PATCH","DELETE"]:
            return obj.by == request.user
        elif request.method=="GET":
            return request.user
        


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