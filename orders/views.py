from rest_framework import generics, permissions

from .models import *
from .serializers import *

import logging
logger = logging.getLogger(__name__)


class CreateOrder(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class ListAllOrders(generics.ListAPIView):
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
    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'


class UpdateOrder(generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = OrderUpdateSerializer
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)