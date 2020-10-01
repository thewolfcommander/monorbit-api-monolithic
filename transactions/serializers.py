from datetime import datetime

from django.utils import timezone
from rest_framework import serializers

from .models import *
from network.models import NetworkStaff
from accounts.serializers import UserMiniSerializer
from network.serializers import MiniNetworkSerializer, NetworkJobOfferingShowSerializer

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
    
    def create(self, validated_data):
        offering = validated_data.get('offering', None)
        if not offering.is_filled and offering.is_active and offering.job.job_type == 'delivery':
            instance = NetworkDeliveryBoyApplication.objects.create(**validated_data)
            return instance
        else:
            raise serializers.ValidationError("Sorry, You cannot apply to this job. Either job is not available or last date has passed or this job is not for you.")


class CreateNetworkPermanentEmployeeApplication(serializers.ModelSerializer):
    class Meta:
        model = NetworkPermanentEmployeeApplication
        fields = [
            'id',
            'offering',
            'permanent_employee',
            'application_status',
            'created'
        ]
    
    def create(self, validated_data):
        offering = validated_data.get('offering', None)
        if not offering.is_filled and offering.is_active and offering.job.job_type == 'permanent':
            instance = NetworkPermanentEmployeeApplication.objects.create(**validated_data)
            return instance
        else:
            raise serializers.ValidationError("Sorry, You cannot apply to this job. Either job is not available or last date has passed or this job is not for you.")


class CreateNetworkFreelancerApplication(serializers.ModelSerializer):
    class Meta:
        model = NetworkFreelancerApplication
        fields = [
            'id',
            'offering',
            'freelancer',
            'application_status',
            'created'
        ]
    
    def create(self, validated_data):
        offering = validated_data.get('offering', None)
        if not offering.is_filled and offering.is_active and offering.job.job_type == 'freelancer':
            instance = NetworkFreelancerApplication.objects.create(**validated_data)
            return instance
        else:
            raise serializers.ValidationError("Sorry, You cannot apply to this job. Either job is not available or last date has passed or this job is not for you.")

    
class ShowNetworkDeliveryBoyApplication(serializers.ModelSerializer):
    offering = NetworkJobOfferingShowSerializer(read_only=True)
    delivery_boy = DeliveryBoyShowSerializer(read_only=True)
    class Meta:
        model = NetworkDeliveryBoyApplication
        fields = [
            'id',
            'offering',
            'delivery_boy',
            'application_status',
            'created',
            'updated'
        ]
    
    def update(self, instance, validated_data):
        instance.application_status = validated_data.get('application_status', instance.application_status)
        if instance.application_status == 'hired':
            try:
                staff = NetworkStaff.objects.get(
                    profile=instance.delivery_boy.job_profile,
                    job=instance.offering.job
                )
                staff.is_active = True
                staff.application_id = instance.id
                staff.save()
            except NetworkStaff.DoesNotExist:
                staff = NetworkStaff.objects.create(
                    profile=instance.delivery_boy.job_profile,
                    job=instance.offering.job,
                    application_id=instance.id,
                    is_active=True
                )
        elif instance.application_status == 'fired':
            try:
                staff = NetworkStaff.objects.get(
                    profile=instance.delivery_boy.job_profile,
                    job=instance.offering.job
                )
                staff.is_active = False
                staff.application_id = instance.id
                staff.save()
            except NetworkStaff.DoesNotExist:
                staff = NetworkStaff.objects.create(
                    profile=instance.delivery_boy.job_profile,
                    job=instance.offering.job,
                    application_id=instance.id,
                    is_active=False
                )
        instance.save()
        return instance


class ShowNetworkPermanentEmployeeApplication(serializers.ModelSerializer):
    offering = NetworkJobOfferingShowSerializer(read_only=True)
    permanent_employee = PermanentEmployeeShowSerializer(read_only=True)
    class Meta:
        model = NetworkPermanentEmployeeApplication
        fields = [
            'id',
            'offering',
            'permanent_employee',
            'application_status',
            'created',
            'updated'
        ]
    
    def update(self, instance, validated_data):
        instance.application_status = validated_data.get('application_status', instance.application_status)
        if instance.application_status == 'hired':
            try:
                staff = NetworkStaff.objects.get(
                    profile=instance.permanent_employee.job_profile,
                    job=instance.offering.job
                )
                staff.is_active = True
                staff.application_id = instance.id
                staff.save()
            except NetworkStaff.DoesNotExist:
                staff = NetworkStaff.objects.create(
                    profile=instance.permanent_employee.job_profile,
                    job=instance.offering.job,
                    application_id=instance.id,
                    is_active=True
                )
        elif instance.application_status == 'fired':
            try:
                staff = NetworkStaff.objects.get(
                    profile=instance.permanent_employee.job_profile,
                    job=instance.offering.job
                )
                staff.is_active = False
                staff.application_id = instance.id
                staff.save()
            except NetworkStaff.DoesNotExist:
                staff = NetworkStaff.objects.create(
                    profile=instance.permanent_employee.job_profile,
                    job=instance.offering.job,
                    application_id=instance.id,
                    is_active=False
                )
        instance.save()
        return instance


class ShowNetworkFreelancerApplication(serializers.ModelSerializer):
    offering = NetworkJobOfferingShowSerializer(read_only=True)
    freelancer = FreelancerShowSerializer(read_only=True)
    class Meta:
        model = NetworkFreelancerApplication
        fields = [
            'id',
            'offering',
            'freelancer',
            'application_status',
            'created',
            'updated'
        ]
    
    def update(self, instance, validated_data):
        instance.application_status = validated_data.get('application_status', instance.application_status)
        if instance.application_status == 'hired':
            try:
                staff = NetworkStaff.objects.get(
                    profile=instance.freelancer.job_profile,
                    job=instance.offering.job
                )
                staff.is_active = True
                staff.application_id = instance.id
                staff.save()
            except NetworkStaff.DoesNotExist:
                staff = NetworkStaff.objects.create(
                    profile=instance.freelancer.job_profile,
                    job=instance.offering.job,
                    application_id=instance.id,
                    is_active=True
                )
        elif instance.application_status == 'fired':
            try:
                staff = NetworkStaff.objects.get(
                    profile=instance.freelancer.job_profile,
                    job=instance.offering.job
                )
                staff.is_active = False
                staff.application_id = instance.id
                staff.save()
            except NetworkStaff.DoesNotExist:
                staff = NetworkStaff.objects.create(
                    profile=instance.freelancer.job_profile,
                    job=instance.offering.job,
                    application_id=instance.id,
                    is_active=False
                )
        instance.save()
        return instance