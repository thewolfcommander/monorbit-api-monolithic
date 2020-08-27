from rest_framework import serializers

from accounts.serializers import UserMiniSerializer
from job_profiles.models import (
    JobProfile,
    DeliveryBoy,
    DeliveryBoyVehicle,
    PermanentEmployee,
    PermanentEmployeeFile,
    PermanentEmployeeSpecification,
    Freelancer,
    FreelancerFile,
    FreelancerSpecification
)


class JobProfileSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True, required=False)
    class Meta:
        model = JobProfile
        fields = [
            'id',
            'user',
            'alt_email',
            'alt_phone_number',
            'photo_url',
            'adhaar_card',
            'address',
            'landmark',
            'city',
            'state',
            'country',
            'pincode',
            'is_verified',
            'is_vehicle',
            'is_delivery_boy',
            'is_permanent_employee',
            'is_freelancer',
            'added',
            'updated'
        ]
    
    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        try:
            instance = JobProfile.objects.create(**validated_data, user=user)
        except:
            instance = JobProfile.objects.get(user=user)
        return instance

    
class DeliveryBoyVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryBoyVehicle
        fields = [
            'id',
            'delivery_boy',
            'driving_license',
            'type_of_vehicle',
            'vehicle_license',
            'valid_upto',
            'vehicle_photo_url',
            'active',
            'added',
            'updated',
        ]

    
class DeliveryBoyShowSerializer(serializers.ModelSerializer):
    job_profile = JobProfileSerializer()
    vehicles = DeliveryBoyVehicleSerializer(read_only=True, many=True)
    class Meta:
        model = DeliveryBoy
        fields = [
            'id',
            'job_profile',
            'is_recharged',
            'active',
            'added',
            'updated',
            'short_bio',
            'vehicles'
        ]

    def update(self, instance, validated_data):
        job = validated_data.pop('job_profile', None)
        profile = instance.job_profile
        
        instance.is_recharged = validated_data.get('is_recharged', instance.is_recharged)
        instance.short_bio = validated_data.get('short_bio', instance.short_bio)
        instance.save()

        if job is not None:
            profile.alt_email = job.get('alt_email', profile.alt_email)
            profile.alt_phone_number = job.get('alt_phone_number', profile.alt_phone_number)
            profile.photo_url = job.get('photo_url', profile.photo_url)
            profile.adhaar_card = job.get('adhaar_card', profile.adhaar_card)
            profile.address = job.get('address', profile.address)
            
            profile.landmark = job.get('landmark', profile.landmark)
            profile.city = job.get('city', profile.city)
            profile.state = job.get('state', profile.state)
            profile.country = job.get('country', profile.country)
            profile.pincode = job.get('pincode', profile.pincode)
            profile.is_verified = job.get('is_verified', profile.is_verified)
            profile.is_vehicle = job.get('is_vehicle', profile.is_vehicle)
            profile.is_delivery_boy = job.get('is_delivery_boy', profile.is_delivery_boy)
            profile.is_permanent_employee = job.get('is_permanent_employee', profile.is_permanent_employee)
            profile.is_freelancer = job.get('is_freelancer', profile.is_freelancer)
            profile.save()

        return instance


    
   
class DeliveryBoyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryBoy
        fields = [
            'id',
            'job_profile',
            'is_recharged',
            'active',
            'added',
            'updated',
            'short_bio'
        ]

    def create(self, validated_data):
        job_profile = validated_data.get('job_profile')
        profile = JobProfile.objects.filter(id=job_profile).first()
        print(profile)
        if profile.is_delivery_boy:
            delivery_boy = DeliveryBoy.objects.create(**validated_data)
        else:
            profile.is_delivery_boy = True
            profile.save()
            delivery_boy = DeliveryBoy.objects.create(**validated_data)
        return delivery_boy



class PermanentEmployeeSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermanentEmployeeSpecification
        fields = [
            'id',
            'spec_type',
            'label',
            'description',
            'added'
        ]


    
class PermanentEmployeeFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermanentEmployeeFile
        fields = [
            'id',
            'file_type',
            'label',
            'file_url',
            'added'
        ]

    
class PermanentEmployeeShowSerializer(serializers.ModelSerializer):
    job_profile = JobProfileSerializer()
    specifications = PermanentEmployeeSpecificationSerializer(many=True)
    files = PermanentEmployeeFileSerializer(many=True)
    class Meta:
        model = PermanentEmployee
        fields = [
            'id',
            'job_profile',
            'is_recharged',
            'active',
            'added',
            'updated',
            'short_bio',
            'files',
            'specifications'
        ]

    def update(self, instance, validated_data):
        job = validated_data.pop('job_profile', None)
        files = validated_data.pop('files', None)
        specifications = validated_data.pop('specifications', None)
        profile = instance.job_profile

        files_data = (instance.files).all()
        files_data = list(files_data)
        specifications_data = (instance.specifications).all()
        specifications_data = list(specifications_data)
        
        instance.is_recharged = validated_data.get('is_recharged', instance.is_recharged)
        instance.short_bio = validated_data.get('short_bio', instance.short_bio)
        instance.save()

        if job is not None:
            profile.alt_email = job.get('alt_email', profile.alt_email)
            profile.alt_phone_number = job.get('alt_phone_number', profile.alt_phone_number)
            profile.photo_url = job.get('photo_url', profile.photo_url)
            profile.adhaar_card = job.get('adhaar_card', profile.adhaar_card)
            profile.address = job.get('address', profile.address)
            
            profile.landmark = job.get('landmark', profile.landmark)
            profile.city = job.get('city', profile.city)
            profile.state = job.get('state', profile.state)
            profile.country = job.get('country', profile.country)
            profile.pincode = job.get('pincode', profile.pincode)
            profile.is_verified = job.get('is_verified', profile.is_verified)
            profile.is_vehicle = job.get('is_vehicle', profile.is_vehicle)
            profile.is_delivery_boy = job.get('is_delivery_boy', profile.is_delivery_boy)
            profile.is_permanent_employee = job.get('is_permanent_employee', profile.is_permanent_employee)
            profile.is_freelancer = job.get('is_freelancer', profile.is_freelancer)
            profile.save()

        if files is not None:
            for f in files:
                fl = files_data.pop(0)
                fl.file_type = f.get('file_type', fl.file_type) 
                fl.label = f.get('label', fl.label) 
                fl.file_url = f.get('file_url', fl.file_url)
                fl.save() 

        if specifications is not None:
            for f in specifications:
                fl = specifications_data.pop(0)
                fl.spec_type = f.get('spec_type', fl.spec_type) 
                fl.label = f.get('label', fl.label) 
                fl.description = f.get('description', fl.description)
                fl.save()

        return instance
    
  
class PermanentEmployeeCreateSerializer(serializers.ModelSerializer):
    specifications = PermanentEmployeeSpecificationSerializer(many=True, required=False)
    files = PermanentEmployeeFileSerializer(many=True, required=False)
    class Meta:
        model = PermanentEmployee
        fields = [
            'id',
            'job_profile',
            'is_recharged',
            'active',
            'added',
            'updated',
            'short_bio',
            'files',
            'specifications'
        ]

    def create(self, validated_data):
        job_profile = validated_data.get('job_profile')
        profile = JobProfile.objects.filter(id=job_profile).first()
        
        files = validated_data.pop('files', None)
        specifications = validated_data.pop('specifications', None)
        if profile.is_permanent_employee:
            permanent_employee = PermanentEmployee.objects.create(**validated_data)
        else:
            profile.is_permanent_employee = True
            profile.save()
            permanent_employee = PermanentEmployee.objects.create(**validated_data)

        if files is not None:
            for f in files:
                PermanentEmployeeFile.objects.create(**f, permanent_employee=permanent_employee)

        if specifications is not None:
            for f in specifications:
                PermanentEmployeeSpecification.objects.create(**f, permanent_employee=permanent_employee)
        return permanent_employee

    


class FreelancerSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreelancerSpecification
        fields = [
            'id',
            'spec_type',
            'label',
            'description',
            'added'
        ]


    
class FreelancerFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreelancerFile
        fields = [
            'id',
            'file_type',
            'label',
            'file_url',
            'added'
        ]




    
class FreelancerShowSerializer(serializers.ModelSerializer):
    job_profile = JobProfileSerializer()
    specifications = FreelancerSpecificationSerializer(many=True)
    files = FreelancerFileSerializer(many=True)
    class Meta:
        model = Freelancer
        fields = [
            'id',
            'job_profile',
            'is_recharged',
            'active',
            'added',
            'updated',
            'short_bio',
            'files',
            'specifications',
        ]

    def update(self, instance, validated_data):
        job = validated_data.pop('job_profile', None)
        files = validated_data.pop('files', None)
        specifications = validated_data.pop('specifications', None)
        profile = instance.job_profile

        files_data = (instance.files).all()
        files_data = list(files_data)
        specifications_data = (instance.specifications).all()
        specifications_data = list(specifications_data)
        
        instance.is_recharged = validated_data.get('is_recharged', instance.is_recharged)
        instance.short_bio = validated_data.get('short_bio', instance.short_bio)
        instance.save()

        if job is not None:
            profile.alt_email = job.get('alt_email', profile.alt_email)
            profile.alt_phone_number = job.get('alt_phone_number', profile.alt_phone_number)
            profile.photo_url = job.get('photo_url', profile.photo_url)
            profile.adhaar_card = job.get('adhaar_card', profile.adhaar_card)
            profile.address = job.get('address', profile.address)
            
            profile.landmark = job.get('landmark', profile.landmark)
            profile.city = job.get('city', profile.city)
            profile.state = job.get('state', profile.state)
            profile.country = job.get('country', profile.country)
            profile.pincode = job.get('pincode', profile.pincode)
            profile.is_verified = job.get('is_verified', profile.is_verified)
            profile.is_vehicle = job.get('is_vehicle', profile.is_vehicle)
            profile.is_delivery_boy = job.get('is_delivery_boy', profile.is_delivery_boy)
            profile.is_permanent_employee = job.get('is_permanent_employee', profile.is_permanent_employee)
            profile.is_freelancer = job.get('is_freelancer', profile.is_freelancer)
            profile.save()

        if files is not None:
            for f in files:
                fl = files_data.pop(0)
                fl.file_type = f.get('file_type', fl.file_type)
                fl.label = f.get('label', fl.label)
                fl.file_url = f.get('file_url', fl.file_url)
                fl.save() 

        if specifications is not None:
            for f in specifications:
                fl = specifications_data.pop(0)
                fl.spec_type = f.get('spec_type', fl.spec_type) 
                fl.label = f.get('label', fl.label) 
                fl.description = f.get('description', fl.description)
                fl.save()

        return instance

    
class FreelancerCreateSerializer(serializers.ModelSerializer):
    specifications = FreelancerSpecificationSerializer(many=True, required=False)
    files = FreelancerFileSerializer(many=True, required=False)
    class Meta:
        model = Freelancer
        fields = [
            'id',
            'job_profile',
            'is_recharged',
            'active',
            'added',
            'updated',
            'short_bio',
            'files',
            'specifications'
        ]

    def create(self, validated_data):
        job_profile = validated_data.get('job_profile')
        profile = JobProfile.objects.filter(id=job_profile).first()
        files = validated_data.pop('files', None)
        specifications = validated_data.pop('specifications', None)

        if profile.is_freelancer:
            freelancer = Freelancer.objects.create(**validated_data)
        else:
            profile.is_freelancer = True
            profile.save()
            freelancer = Freelancer.objects.create(**validated_data)
        
        if files is not None:
            for f in files:
                FreelancerFile.objects.create(**f, freelancer=freelancer)

        if specifications is not None:
            for f in specifications:
                FreelancerSpecification.objects.create(**f, freelancer=freelancer)
        return freelancer