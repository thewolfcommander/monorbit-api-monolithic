from rest_framework import serializers
from .models import *
from monorbit.utils import fcm


class MessageShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'id',
            'message_title',
            'message_body',
        ]


class FCMDeviceCreateSerializer(serializers.ModelSerializer):
    messages = MessageShowSerializer(many=True,required=False)
    class Meta:
        model = FcmDevice
        fields = [
            'id',
            'user',
            'registration_id',
            'device_type',
            'messages',
        ]

    def create(self,validated_data):
        registration_id = validated_data.get("registration_id",None)
        messages = validated_data.pop('messages',None)

        if registration_id is not None:
            try:
                fcmdevice = FcmDevice.objects.get(registration_id=registration_id)
            except:
                fcmdevice = FcmDevice.objects.create(**validated_data)

            if messages is not None:
                for i in messages:
                    Message.objects.create(**i,fcmdevice=fcmdevice)

                    # notify
                    fcm.single_notification(registration_id,i['message_title'],i['message_body'])
            
            
        
        return fcmdevice