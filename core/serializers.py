from rest_framework import serializers

from .models import *


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