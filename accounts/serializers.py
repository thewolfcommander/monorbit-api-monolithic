from rest_framework import serializers, exceptions

from . import models as acc_models



"""
Serialized Data for User model

'mobile_number',
'full_name',
'email',
'hash_token',
'gender',
'dob',
'registration_reference',
'city',
'pincode',
'network_created',
'is_consumer',
'is_creator',
'is_working_profile',
'is_active',
'is_agreed_to_terms',
'is_admin',
'is_mobile_verified',
'is_email_verified',
'is_logged_in',
'is_archived',
'registered_on',
'last_logged_in_time',
'updated_on',

"""


class ObtainTokenSerializer(serializers.Serializer):
    mobile_number = serializers.CharField()
    password = serializers.CharField(max_length=20)

    def validate(self, attrs):

        mobile_number = attrs.get('mobile_number')
        password = attrs.get('password')
        user_obj = acc_models.User.objects.filter(mobile_number=mobile_number, is_active=True, is_archived=False, is_agreed_to_terms=True).first()

        if user_obj is None:
            raise serializers.ValidationError("No user exists with this mobile number")
            # return {"message": "No User exists with this email"}

        if not user_obj.check_password(password):
            raise serializers.ValidationError("Password entered is incorrect")
            # return {"message": "No User exists with this email"}

        return attrs

    
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = acc_models.User
        fields = [
            'mobile_number',
            'password',
            'full_name',
            'email',
            'registration_reference',
            'city',
            'pincode',
            'is_agreed_to_terms',
        ]

    def validate(self, attrs):

        mobile_number = attrs.get('mobile_number')
        password = attrs.get('password')
        if not mobile_number:
            raise serializers.ValidationError("You should enter your mobile number")

        user_obj = acc_models.User.objects.filter(mobile_number=mobile_number, is_active=True).first()

        if user_obj is not None:
            if not user_obj.is_mobile_verified:
                raise serializers.ValidationError("You have registered but your mobile is not verified. Kindly Proceed to Login and verify your mobile number.")
            raise serializers.ValidationError("A user exists with this mobile number")
            # return {"message": "No User exists with this email"}
        return attrs

    
class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = acc_models.User
        fields = [
            'mobile_number',
            'full_name',
            'email',
            'hash_token',
            'gender',
            'dob',
            'registration_reference',
            'city',
            'pincode',
            'network_created',
            'otp_sent',
            'is_consumer',
            'is_creator',
            'is_working_profile',
            'is_active',
            'is_agreed_to_terms',
            'is_admin',
            'is_mobile_verified',
            'is_email_verified',
            'is_logged_in',
            'is_archived',
            'registered_on',
            'last_logged_in_time',
            'updated_on',
        ]

    def update(self, instance, validated_data):
        instance.mobile_number = validated_data.get('mobile_number', instance.mobile_number)
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.email = validated_data.get('email', instance.email)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.dob = validated_data.get('dob', instance.dob)
        instance.city = validated_data.get('city', instance.city)
        instance.pincode = validated_data.get('pincode', instance.pincode)
        instance.save()

        return instance


class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = acc_models.User
        fields = [
            'is_active',
            'is_archived',
        ]

    def update(self, instance, validated_data):
        instance.is_active = False
        instance.is_archived = True
        instance.save()

        return instance

    
class UpdatePasswordSerializer(serializers.Serializer):
    model = acc_models.User
    new_password = serializers.CharField(required=True)


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = acc_models.User
        fields = [
            'mobile_number',
            'full_name',
            'email',
        ]
