from rest_framework import generics, permissions

from .serializers import *
from cart.models import *


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