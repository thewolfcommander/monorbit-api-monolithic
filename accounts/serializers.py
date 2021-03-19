from rest_framework import serializers, exceptions

from . import models as acc_models


import logging
logger = logging.getLogger(__name__)

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
    """
    Serializer for Logiing in to the Monorbit
    """
    mobile_number = serializers.CharField()
    password = serializers.CharField(max_length=20)

    def validate(self, attrs):
        """
        Validating the fields - mobile number and password
        """
        mobile_number = attrs.get('mobile_number')
        password = attrs.get('password')
        # Getting the user object from the database
        user_obj = acc_models.User.objects.filter(mobile_number=mobile_number, is_active=True, is_archived=False, is_agreed_to_terms=True).first()

        # check if the user exists
        if user_obj is None:
            raise serializers.ValidationError("No user exists with this mobile number")

        # Check if password matches
        if not user_obj.check_password(password):
            raise serializers.ValidationError("Password entered is incorrect")
            # return {"message": "No User exists with this email"}

        return attrs

    
class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new user
    """
    class Meta:
        model = acc_models.User
        fields = [
            'country_code',
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
        """
        Validating fields for any mistake in input
        """

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

class GuestUserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for creating guest user.
    """
    class Meta:
        model = acc_models.User
        fields = [
            'mobile_number',
            'full_name',
            'is_guest',
            'is_agreed_to_terms',
        ]

    def validate(self,attrs):
        """
        validating for in case of guest user.
        """
        is_guest = attrs.get("is_guest",None)
        is_agreed_to_terms = attrs.get("is_agreed_to_terms")
        if is_guest is not None:
            if is_guest == False:
                raise serializers.ValidationError("is_guest value should be true.")
        else:
            raise serializers.ValidationError("You will have to provide is_guest(true).")

        return attrs


    
class UserLocalizationSerializer(serializers.ModelSerializer):
    """
    Serializer for User Localization
    """
    class Meta:
        model = acc_models.UserLocalization
        fields = [
            'communication_language_code',
            'interface_language_code'
        ]

    
class UserInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for providing all user details
    """
    # localization = UserLocalizationSerializer(read_only=True, many=True)
    class Meta:
        model = acc_models.User
        fields = [
            'id',
            'mobile_number',
            'full_name',
            'email',
            'hash_token',
            'country_code',
            'gender',
            'dob',
            'registration_reference',
            'city',
            'pincode',
            'network_created',
            'otp_sent',
            'password_otp_sent',
            'order_count',
            'is_consumer',
            'followed_networks',
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
            # 'localization',
        ]

    def update(self, instance, validated_data):
        """
        Updating the user's details
        """
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
    """
    Deactivating and deleting the user temporarily
    """
    class Meta:
        model = acc_models.User
        fields = [
            'is_active',
            'is_archived',
        ]

    def update(self, instance, validated_data):
        """
        Updating the user's details
        """
        instance.is_active = False
        instance.is_archived = True
        instance.save()

        return instance

    
class UpdatePasswordSerializer(serializers.Serializer):
    """
    Serializer to update password
    """
    model = acc_models.User
    new_password = serializers.CharField(required=True)


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = acc_models.User
        fields = [
            'id',
            'mobile_number',
            'full_name',
            'email',
        ]
