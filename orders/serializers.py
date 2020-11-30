from rest_framework import serializers

from cart.serializers import CartShowSerializer, CartMegaDetailSerializer
from addresses.serializers import AddressShowSerializer
from .models import *
from core.models import NetworkOrder
from network.models import Network

import logging
logger = logging.getLogger(__name__)


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
            'active',
            'is_paid',
            'payment_method'
        ]

    def create(self, validated_data):
        cart = validated_data.get('cart')
        if cart.is_active:
            instance = Order.objects.create(**validated_data)
            instance.day_id = 3
            instance.shipping_total = instance.cart.shipping
            instance.discount = instance.cart.discount
            instance.total = instance.cart.total
            instance.tax = 0.00
            instance.cart.is_active = False
            instance.cart.save()
            instance.cart.user.order_count += 1
            instance.cart.user.save()
            instance.save()
            for p in instance.cart.productentry_set.all():
                p.product_status = 'order_created'
                p.save()
                NetworkOrder.objects.create(
                    network=p.product.network,
                    order=instance
                )
            return instance
        else:
            raise Exception("The Cart is not Correct. It has been used already")


class ListOrderSerializer(serializers.ModelSerializer):
    cart = CartShowSerializer(read_only=True)
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
            'is_paid',
            'payment_method'
        ]


class OrderDetailSerializer(serializers.ModelSerializer):
    cart = CartMegaDetailSerializer(read_only=True)
    billing_address = AddressShowSerializer(read_only=True)
    shipping_address = AddressShowSerializer(read_only=True)
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
            'is_paid',
            'payment_method'
        ]

    
class OrderUpdateSerializer(serializers.ModelSerializer):
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
            'is_paid',
            'payment_method'
        ]

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        if (instance.status == 'Delivered') or (instance.status == 'Cancelled') or (instance.status == 'Refunded') or (instance.status == 'Returned'):
            instance.active = False
            instance.is_paid = validated_data.get('is_paid', instance.is_paid)
        instance.save()
        return instance