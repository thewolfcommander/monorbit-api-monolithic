from rest_framework import serializers
from .models import Cart, ProductEntry, Wishlist, WishlistProductEntry
from accounts.serializers import UserMiniSerializer
from product_catalog.serializers import ProductShowSerializer, ProductMiniSerializer
from product_catalog.models import Product


import logging
logger = logging.getLogger(__name__)


class ProductEntryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductEntry
        fields = [
            'id',
            'cart',
            'product',
            'quantity',
            'cost'
        ]

    def create(self, validated_data):
        instance = ProductEntry.objects.create(**validated_data)
        instance.cart.count += 1
        instance.cart.sub_total = float(instance.cart.sub_total) + float(instance.cost)
        instance.cart.total = (float(instance.cart.sub_total) + float(instance.cart.shipping)) - float(instance.cart.discount)
        instance.cart.save()

        return instance


class ProductEntryTinyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductEntry
        fields = [
            'id',
            'product',
            'quantity',
            'cost'
        ]

    
class ProductEntryShowSerializer(serializers.ModelSerializer):
    product = ProductShowSerializer(read_only=True)
    class Meta:
        model = ProductEntry
        fields = [
            'id',
            'cart',
            'product',
            'quantity',
            'cost'
        ]

    
class ProductEntryTinySerializer(serializers.ModelSerializer):
    product = ProductMiniSerializer(read_only=True)
    class Meta:
        model = ProductEntry
        fields = [
            'id',
            'product',
            'quantity',
            'cost'
        ]

    
class CartCreateSerializer(serializers.ModelSerializer):
    # user = UserMiniSerializer(read_only=True)
    products = ProductEntryTinyCreateSerializer(many=True, required=False)
    class Meta:
        model = Cart
        fields = [
            'id',
            'user',
            'count',
            'sub_total',
            'shipping',
            'total',
            'discount',
            'is_active',
            'timestamp',
            'updated',
            'products'
        ]

    def create(self, validated_data):
        products = validated_data.pop('products', None)
        user = validated_data.get('user', None)
        count = 0
        sub_total = 0.00
        shipping = 25.00
        total = 0.00
        discount = 0.00
        if user is not None:
            try:
                instance = Cart.objects.get(user=user, is_active=True)
                instance.count = 0
                instance.sub_total = 0.00
                instance.shipping = 0.00
                instance.total = 0.00
                instance.discount = 0.00
                try:
                    instance.productentry_set.all().delete()
                except:
                    pass
                if products is not None:
                    for p in products:
                        pd = p.get('product', None)
                        quan = p.get('quantity')
                        print(p.get('product'))
                        if pd is not None:
                            try:
                                pe = ProductEntry.objects.get(product=pd, cart=instance)
                                pe.delete()
                                pe = ProductEntry.objects.create(**p, cart=instance)
                                pe.save()
                            except:
                                pe = ProductEntry.objects.create(**p, cart=instance)
                        else:
                            print("Breakin")
                            break
                        count += 1
                        sub_total = sub_total + float(pe.cost)

                total = (sub_total + shipping) - discount
                instance.sub_total = sub_total
                instance.total = total
                instance.discount = discount
                instance.shipping = shipping
                instance.count = count
                instance.save()
            except Cart.DoesNotExist:
                instance = Cart.objects.create(
                    user=user, 
                    sub_total=sub_total, 
                    total=total, 
                    shipping=shipping,
                    count=count,
                    is_active=True
                )
                if products is not None:
                    for p in products:
                        pe = ProductEntry.objects.create(**p, cart=instance)
                        count += 1
                        sub_total = sub_total + float(pe.cost)
                
                else:
                    shipping = 0.00
                total = (sub_total + shipping) - discount

                instance.sub_total = sub_total
                instance.total = total
                instance.discount = discount
                instance.shipping = shipping
                instance.count = count
                instance.save()
            return instance
        else:
            return {
                "status": False,
                "message": "Cannot Create Cart. Try again later"
            }

        
class CartShowSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True)
    products = ProductEntryTinySerializer(many=True, required=False)
    class Meta:
        model = Cart
        fields = [
            'id',
            'user',
            'count',
            'sub_total',
            'shipping',
            'total',
            'discount',
            'is_active',
            'timestamp',
            'updated',
            'products'
        ]


class CartMegaDetailSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True)
    products = ProductEntryShowSerializer(many=True, required=False)
    class Meta:
        model = Cart
        fields = [
            'id',
            'user',
            'count',
            'sub_total',
            'shipping',
            'total',
            'discount',
            'is_active',
            'timestamp',
            'updated',
            'products'
        ]


class WishlistProductEntryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistProductEntry
        fields = [
            'id',
            'product',
            'wishlist'
        ]

    def create(self, validated_data):
        instance = WishlistProductEntry.objects.create(**validated_data)
        instance.wishlist.count += 1
        instance.wishlist.save()
        return instance


class WishlistProductEntryShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistProductEntry
        fields = [
            'id',
            'product',
        ]


class WishlistShowSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True)
    products = WishlistProductEntryShowSerializer(many=True, required=False)
    class Meta:
        model = Wishlist
        fields = [
            'id',
            'user',
            'count',
            'updated',
            'timestamp',
            'products'
        ]

    
class WishlistCreateSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True)
    products = WishlistProductEntryCreateSerializer(many=True, required=False)
    class Meta:
        model = Wishlist
        fields = [
            'id',
            'user',
            'count',
            'updated',
            'timestamp',
            'products'
        ]

    def create(self, validated_data):
        products = validated_data.pop('products', None)
        count = 0
        user = self.context['request'].user
        return user