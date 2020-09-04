from rest_framework import serializers

from network.serializers import ShowNetworkSerializer
from network.models import Network
from .models import *


import logging
logger = logging.getLogger(__name__)

class NetworkMembershipPlanFeaturesSerailizer(serializers.ModelSerializer):
    class Meta:
        model = NetworkMembershipPlanFeatures
        fields = [
            'key',
            'description',
            'active'
        ]


class NetworkMembershipPlanSerializer(serializers.ModelSerializer):
    features = NetworkMembershipPlanFeaturesSerailizer(read_only=True, required=False)
    class Meta:
        model = NetworkMembershipPlan
        fields = [
            'id',
            'name',
            'price_per_day',
            'features'
        ]

    
class NetworkMembershipRelationSerializer(serializers.ModelSerializer):
    network = ShowNetworkSerializer(read_only=True)
    plan = NetworkMembershipPlanSerializer(read_only=True)
    class Meta:
        model = NetworkMembershipRelation
        fields = [
            'id',
            'network',
            'plan'
        ]


class NetworkMembershipRelationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkMembershipRelation
        fields = [
            'id',
            'network',
            'plan'
        ]

    
class NetworkMembershipActivityCreateSerializer(serializers.ModelSerializer):
    relation = NetworkMembershipRelationCreateSerializer(required=True)
    class Meta:
        model = NetworkMembershipActivity
        fields = [
            'id',
            'relation',
            'payment',
            'active_till',
            'expiry',
            'active'
        ]

    def create(self, validated_data):
        print("hello")
        user = self.context['request'].user
        relation = validated_data.pop("relation")
        network_obj = Network.objects.filter(user=user, is_active=True)
        if network_obj.exists():
            try:
                finding = NetworkMembershipRelation.objects.get(network=network)
            except:
                plan = relation.get('plan')
                finding = NetworkMembershipRelation.objects.create(network=network, plan=plan)
            instance = NetworkMembershipActivity.objects.create(**validated_data, relation=finding)
            return instance
        else:
            raise ValidationError("Invalid Network Found")     


    
class NetworkMembershipActivityShowSerializer(serializers.ModelSerializer):
    relation = NetworkMembershipRelationSerializer(read_only=True)
    class Meta:
        model = NetworkMembershipActivity
        fields = [
            'id',
            'relation',
            'payment',
            'active_till',
            'expiry',
            'active'
        ]