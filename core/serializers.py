from rest_framework import serializers

from .models import *
from accounts.serializers import *


class TipToGrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipToGrow
        fields = [
            'id',
            'tip',
            'upvotes',
            'downvotes',
            'active',
            'added',
            'updated'
        ]

    def updated(self, instance, validated_data):
        instance.tip = validated_data.get('tip', instance.tip)
        instance.upvotes = validated_data.get('upvotes', instance.upvotes)
        instance.downvotes = validated_data.get('downvotes', instance.downvotes)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance

    
class EmailSentToUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailSentToUsers
        fields = [
            'id',
            'email_type',
            'sent_from_ip_address',
            'email_sent_from',
            'email_sent_to',
            'subject',
            'message',
            'sent_on',
            'is_success'
        ]

    
class UserLoginActivitySerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True)
    class Meta:
        model = UserLoginActivity
        fields = [
            'id',
            'user',
            'ip_address',
            'os_platform',
            'browser',
            'is_logged_from_mobile',
            'is_logged_from_web',
            'timestamp'
        ]

    
class UserDeviceRegistrationSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True)
    class Meta:
        model = UserDeviceRegistration
        fields = [
            'id',
            'user',
            'device_type',
            'operating_system',
            'browser',
            'ip_addresss',
            'lat',
            'lng',
            'device_language',
            'user_agent',
            'is_app',
            'is_browser',
            'timestamp'
        ]