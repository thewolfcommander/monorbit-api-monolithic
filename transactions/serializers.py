from rest_framework import serializers

from .models import *
from accounts.serializers import UserMiniSerializer
from network.serializers import MiniNetworkSerializer

from job_profiles.serializers import DeliveryBoyShowSerializer, PermanentEmployeeShowSerializer, FreelancerShowSerializer

class CreateNetworkFollowerSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True)
    class Meta:
        model = NetworkFollower
        fields = [
            'id',
            'network',
            'user',
            'created'
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        try:
            instance = NetworkFollower.objects.get(user=user, network=validated_data.get('network'))
        except NetworkFollower.DoesNotExist:
            instance = NetworkFollower.objects.create(**validated_data, user=user)
            instance.user.followed_networks += 1
            instance.user.save()
            instance.network.followers += 1
            instance.network.save()
        return instance

    
class ShowNetworkFollowerSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True)
    network = MiniNetworkSerializer(read_only=True)
    class Meta:
        model = NetworkFollower
        fields = [
            'id',
            'network',
            'user',
            'created'
        ]

    
class CreateNetworkDeliveryBoyApplication(serializers.ModelSerializer):
    class Meta:
        model = NetworkDeliveryBoyApplication
        fields = [
            'id',
            'offering',
            'delivery_boy',
            'application_status',
            'created'
        ]
    
    # def create()