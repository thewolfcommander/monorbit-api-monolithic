from rest_framework import serializers

from .models import *


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'day_id',
            'billing_address',
            'shipping_address',
            'is_billing_shipping_same',
            'cart',
            'status',
            'shipping_total',
            'discount',
            'total',
            'tax',
            'active'
        ]