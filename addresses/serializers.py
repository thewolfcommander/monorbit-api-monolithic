from rest_framework import serializers
from .models import *
from accounts.serializers import UserMiniSerializer


import logging
logger = logging.getLogger(__name__)

class AddressCreateSerializer(serializers.ModelSerializer):
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

    
class AddressShowSerializer(serializers.ModelSerializer):
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