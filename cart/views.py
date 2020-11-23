from django.http import Http404
from rest_framework import generics, permissions
from rest_framework.views import Response, APIView

from .serializers import *
from cart.models import *


import logging
logger = logging.getLogger(__name__)


class CreateProductEntry(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductEntryCreateSerializer
    queryset = ProductEntry.objects.all()


class ListProductEntry(generics.ListAPIView):
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
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductEntryShowSerializer
    queryset = ProductEntry.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
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
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductEntryUpdateSerializer
    queryset = ProductEntry.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CreateCart(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartCreateSerializer
    queryset = Cart.objects.all()


class ListCart(generics.ListAPIView):
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
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartShowSerializer
    queryset = Cart.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class GetOrCreateWishlist(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            wishlist = Wishlist.objects.get(user=request.user)
        except Wishlist.DoesNotExist:
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
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WishlistShowSerializer
    queryset = Wishlist.objects.all()
    lookup_field = 'id'


class AddWishlistProductEntry(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WishlistProductEntryCreateSerializer
    queryset = WishlistProductEntry.objects.all()


class DeleteWishlistProductEntry(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
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