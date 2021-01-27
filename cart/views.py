from django.http import Http404
from rest_framework import generics, permissions
from rest_framework.views import Response, APIView

from .serializers import *
from cart.models import *
from .permissions import *


import logging
logger = logging.getLogger(__name__)


class CreateProductEntry(generics.CreateAPIView):
    """
    Purpose of this view is to create product entry in cart.
    User can add product in their cart using this view.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductEntryCreateSerializer
    queryset = ProductEntry.objects.all()


class ListProductEntry(generics.ListAPIView):
    """
    List of all product in cart.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductEntryShowSerializer
    queryset = ProductEntry.objects.all()
    filterset_fields = [
        'cart',
        'product_status',
        'product',
        'quantity'
    ]


class UpdateProductEntry(generics.RetrieveUpdateDestroyAPIView):
    """
    "IsCartProductOwner" is used,so that only owner can update.
    User can update their cart via adding or delete product in cart.
    """
    permission_classes = [IsCartProductOwner]
    serializer_class = ProductEntryShowSerializer
    queryset = ProductEntry.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            # In case of delete get the object,decrease cart count by 1, decrease carts sub_total and total, and destroy instance.
            instance = self.get_object()
            instance.cart.count -= 1
            instance.cart.sub_total = float(instance.cart.sub_total) - float(instance.cost)
            instance.cart.total = (float(instance.cart.sub_total) + float(instance.cart.shipping)) - float(instance.cart.discount)
            instance.cart.save()
            self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=204)


class UpdateProductOrderStatus(generics.UpdateAPIView):
    """
    Update prodcut status like
        ('not_valid', 'Not Valid'),
        ('in_cart', 'In Cart'),
        ('order_created', 'Order Created'),
        ('order_confirmed', 'Order Confirmed'),
        ('order_shipped', 'Order shipped'),
        ('order_dispatched', 'Order dispatched'),
        ('order_out_for_delivery', 'Order out for delivery'),
        ('order_delivered', 'Order Delivered'),
        ('order_cancelled', 'Order Cancelled'),
        ('order_returned', 'Order Returned'),
        ('order_refunded', 'Order Refunded'),
    """
    permission_classes = [ProductOrderStatus]
    serializer_class = ProductEntryUpdateSerializer
    queryset = ProductEntry.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CreateCart(generics.CreateAPIView):
    """
    Create cart for user.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartCreateSerializer
    queryset = Cart.objects.all()


class ListCart(generics.ListAPIView):
    """
    List of cart.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartShowSerializer
    queryset = Cart.objects.all()
    filterset_fields = [
        'user',
        'count',
        'sub_total',
        'shipping',
        'total',
        'is_active'
    ]


class UpdateCart(generics.RetrieveUpdateDestroyAPIView):
    """
    Update( put, patch and delete) cart view. Only cart owner can do update.
    And only cart owner can get thier cart info.
    """
    permission_classes = [permissions.IsAuthenticated,IsCartOwner]
    serializer_class = CartShowSerializer
    queryset = Cart.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class GetOrCreateWishlist(APIView):
    """
    Creating wishlist and getting own wishlist.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            # try to get wishlist by user id
            wishlist = Wishlist.objects.get(user=request.user)
        except Wishlist.DoesNotExist:
            # if wishlist does not exist then create wishlist for user
            wishlist = Wishlist.objects.create(user=request.user)
        return Response({
            'status': True,
            'wishlist': {
                'id': wishlist.id,
                'user': wishlist.user.id,
                'count': wishlist.count,
                'updated': wishlist.updated
            }
        }, status=200)

    
class ShowWishlistDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Getting wish list detail. Only wishlist owner can update (put, patch and delete) thier wishlist.
    """
    permission_classes = [permissions.IsAuthenticated,IsCartOwner]
    serializer_class = WishlistShowSerializer
    queryset = Wishlist.objects.all()
    lookup_field = 'id'


class AddWishlistProductEntry(generics.CreateAPIView):
    """
    Adding products to wishlist.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WishlistProductEntryCreateSerializer
    queryset = WishlistProductEntry.objects.all()


class DeleteWishlistProductEntry(generics.DestroyAPIView):
    """
    Deleting product from wish list.
    "AddWishlistPermission" is used for only wishlist owner can delete product from thier wishlist.
    """
    permission_classes = [permissions.IsAuthenticated,AddWishlistPermission]
    serializer_class = WishlistProductEntryCreateSerializer
    queryset = WishlistProductEntry.objects.all()
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.wishlist.count -= 1
            instance.wishlist.save()
            self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=204)