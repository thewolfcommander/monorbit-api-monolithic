from rest_framework import generics, permissions

from .models import *
from .serializers import *

import logging
logger = logging.getLogger(__name__)


class CreateOrder(generics.CreateAPIView):
    """
    normal user create order of a product of cart.
    """
    serializer_class = OrderCreateSerializer
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class ListAllOrders(generics.ListAPIView):
    """
    List of all orders.
    """
    serializer_class = ListOrderSerializer
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = [
        'id',
        'day_id',
        'billing_address',
        'shipping_address',
        'is_billing_shipping_same',
        'cart',
        'cart__user',
        'active',
        'status'
    ]


class OrderDetail(generics.RetrieveAPIView):
    """
    normal user can get single their order.
    """
    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'


class UpdateOrder(generics.UpdateAPIView, generics.DestroyAPIView):
    """
    normal user can update and delete their orders.
    """
    serializer_class = OrderUpdateSerializer
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)