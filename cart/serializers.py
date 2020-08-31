from rest_framework import serializers
from .models import Cart, ProductEntry
from accounts.serializers import UserMiniSerializer
from product_catalog.serializers import ProductShowSerializer


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
    product = ProductShowSerializer(read_only=True)
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
                if products is not None:
                    for p in products:
                        pd = p.get('product')
                        quan = f.get('quantity')
                        try:
                            pe = ProductEntry.objects.get(product=pd, cart=instance)
                            pe.delete()
                            pe = ProductEntry.objects.create(**p, cart=instance)
                        except:
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