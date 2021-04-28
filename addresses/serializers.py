from rest_framework import serializers
from .models import *
from accounts.serializers import UserMiniSerializer


import logging
logger = logging.getLogger(__name__)

class AddressCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for add addresses when user ordered(may be billing or shipping address)
    """
    class Meta:
        model = Address
        fields = [
            'id',
            'user',
            'name',
            'alt_name',
            'address_1',
            'address_2',
            'landmark',
            'city',
            'state',
            'country',
            'pincode',
            'alt_phone',
            'lat',
            'lng',
            'is_default',
            'is_active',
            'is_archived',
            'created',
            'updated'
        ]

    def create(self, validated_data):
        is_default = validated_data.get('is_default', False)
        # user = validated_data.pop('user')

        if is_default:
            queryset = Address.objects.filter(user=self.context['request'].user)
            if queryset.exists():
                for ad in queryset:
                    ad.is_default = False
                    ad.save()
        
        instance = Address.objects.create(**validated_data, user=self.context['request'].user)
        return instance

    
class AddressShowSerializer(serializers.ModelSerializer):
    """
    Serializer for showing address.
    """
    user = UserMiniSerializer(read_only=True)
    class Meta:
        model = Address
        fields = [
            'id',
            'user',
            'name',
            'alt_name',
            'address_1',
            'address_2',
            'landmark',
            'city',
            'state',
            'country',
            'pincode',
            'alt_phone',
            'lat',
            'lng',
            'is_default',
            'is_active',
            'is_archived',
            'created',
            'updated'
        ]

    def update(self, instance, validated_data):
        """
        Updating address.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.alt_name = validated_data.get('alt_name', instance.alt_name)
        instance.address_1 = validated_data.get('address_1', instance.address_1)
        instance.address_2 = validated_data.get('address_2', instance.address_2)
        instance.landmark = validated_data.get('landmark', instance.landmark)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.country = validated_data.get('country', instance.country)
        instance.pincode = validated_data.get('pincode', instance.pincode)
        instance.alt_phone = validated_data.get('alt_phone', instance.alt_phone)
        instance.lat = validated_data.get('lat', instance.lat)
        instance.lng = validated_data.get('lng', instance.lng)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_archived = validated_data.get('is_archived', instance.is_archived)
        
        is_default = validated_data.get('is_default', False)

        if is_default:
            for ad in Address.objects.filter(user=instance.user):
                ad.is_default=False
                ad.save()
            instance.is_default = True
        instance.save()
        return instance