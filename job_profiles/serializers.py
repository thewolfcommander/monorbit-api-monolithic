from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.serializers import UserMiniSerializer
from job_profiles.models import *


import logging

logger = logging.getLogger(__name__)


class JobProfileSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True, required=False)

    class Meta:
        model = JobProfile
        fields = [
            "id",
            "user",
            "alt_email",
            "alt_phone_number",
            "photo_url",
            "adhaar_card",
            "address",
            "landmark",
            "city",
            "state",
            "country",
            "pincode",
            "is_verified",
            "is_vehicle",
            "is_delivery_boy",
            "is_permanent_employee",
            "is_freelancer",
            "added",
            "updated",
        ]

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user
        try:
            instance = JobProfile.objects.create(**validated_data, user=user)
            return instance
        except Exception as e:
            raise ValidationError("Cannot create job profile. Reason: {}".format(e))


class DeliveryBoyVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryBoyVehicle
        fields = [
            "id",
            "delivery_boy",
            "driving_license",
            "type_of_vehicle",
            "vehicle_license",
            "valid_upto",
            "vehicle_photo_url",
            "active",
            "added",
            "updated",
        ]

    def create(self, validated_data):
        instance = DeliveryBoyVehicle.objects.create(**validated_data)
        instance.delivery_boy.job_profile.is_vehicle = True
        instance.delivery_boy.job_profile.save()
        return instance


class DeliveryBoyShowSerializer(serializers.ModelSerializer):
    job_profile = JobProfileSerializer()
    vehicles = DeliveryBoyVehicleSerializer(read_only=True, many=True)

    class Meta:
        model = DeliveryBoy
        fields = [
            "id",
            "job_profile",
            "is_recharged",
            "active",
            "added",
            "updated",
            "short_bio",
            "vehicles",
        ]

    def update(self, instance, validated_data):
        job = validated_data.pop("job_profile", None)
        profile = instance.job_profile

        instance.is_recharged = validated_data.get(
            "is_recharged", instance.is_recharged
        )
        instance.short_bio = validated_data.get("short_bio", instance.short_bio)
        instance.save()

        if job is not None:
            profile.alt_email = job.get("alt_email", profile.alt_email)
            profile.alt_phone_number = job.get(
                "alt_phone_number", profile.alt_phone_number
            )
            profile.photo_url = job.get("photo_url", profile.photo_url)
            profile.adhaar_card = job.get("adhaar_card", profile.adhaar_card)
            profile.address = job.get("address", profile.address)

            profile.landmark = job.get("landmark", profile.landmark)
            profile.city = job.get("city", profile.city)
            profile.state = job.get("state", profile.state)
            profile.country = job.get("country", profile.country)
            profile.pincode = job.get("pincode", profile.pincode)
            profile.is_verified = job.get("is_verified", profile.is_verified)
            profile.is_vehicle = job.get("is_vehicle", profile.is_vehicle)
            profile.is_delivery_boy = job.get(
                "is_delivery_boy", profile.is_delivery_boy
            )
            profile.is_permanent_employee = job.get(
                "is_permanent_employee", profile.is_permanent_employee
            )
            profile.is_freelancer = job.get("is_freelancer", profile.is_freelancer)
            profile.save()

        return instance


class DeliveryBoyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryBoy
        fields = [
            "id",
            "job_profile",
            "is_recharged",
            "active",
            "added",
            "updated",
            "short_bio",
        ]

    def create(self, validated_data):
        job_profile = validated_data.get("job_profile")
        profile = JobProfile.objects.filter(id=job_profile).first()
        print(profile)
        if profile.is_delivery_boy:
            try:
                delivery_boy = DeliveryBoy.objects.get(job_profile=profile)
            except DeliveryBoy.DoesNotExist:
                profile.is_delivery_boy = True
                profile.save()
                delivery_boy = DeliveryBoy.objects.create(**validated_data)
        else:
            profile.is_delivery_boy = True
            profile.save()
            delivery_boy = DeliveryBoy.objects.create(**validated_data)
        return delivery_boy


class PermanentEmployeeSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermanentEmployeeSpecification
        fields = ["id", "spec_type", "label", "description", "added"]


class PermanentEmployeeSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermanentEmployeeSkill
        fields = ["id", "level", "label", "description", "added"]


class PermanentEmployeeExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermanentEmployeeExperience
        fields = [
            "id",
            "title",
            "organization",
            "location",
            "start_date",
            "end_date",
            "description",
            "added",
        ]


class PermanentEmployeeEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermanentEmployeeEducation
        fields = [
            "id",
            "title",
            "specialization",
            "organization",
            "location",
            "start_date",
            "end_date",
            "description",
            "added",
        ]


class PermanentEmployeeFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermanentEmployeeFile
        fields = ["id", "file_type", "label", "file_url", "added"]


class PermanentEmployeeShowSerializer(serializers.ModelSerializer):
    job_profile = JobProfileSerializer()
    specifications = PermanentEmployeeSpecificationSerializer(many=True)
    files = PermanentEmployeeFileSerializer(many=True)
    educations = PermanentEmployeeEducationSerializer(many=True)
    skills = PermanentEmployeeSkillSerializer(many=True)
    experiences = PermanentEmployeeExperienceSerializer(many=True)

    class Meta:
        model = PermanentEmployee
        fields = [
            "id",
            "job_profile",
            "is_recharged",
            "active",
            "added",
            "updated",
            "short_bio",
            "files",
            "specifications",
            "educations",
            "skills",
            "experiences",
        ]

    def update(self, instance, validated_data):
        job = validated_data.pop("job_profile", None)
        files = validated_data.pop("files", None)
        specifications = validated_data.pop("specifications", None)
        profile = instance.job_profile

        files_data = (instance.files).all()
        files_data = list(files_data)
        specifications_data = (instance.specifications).all()
        specifications_data = list(specifications_data)

        skills_data = (instance.skills).all()
        skills_data = list(skills_data)

        educations_data = (instance.educations).all()
        educations_data = list(educations_data)

        experiences_data = (instance.experiences).all()
        experiences_data = list(experiences_data)

        instance.is_recharged = validated_data.get(
            "is_recharged", instance.is_recharged
        )
        instance.short_bio = validated_data.get("short_bio", instance.short_bio)
        instance.save()

        if job is not None:
            profile.alt_email = job.get("alt_email", profile.alt_email)
            profile.alt_phone_number = job.get(
                "alt_phone_number", profile.alt_phone_number
            )
            profile.photo_url = job.get("photo_url", profile.photo_url)
            profile.adhaar_card = job.get("adhaar_card", profile.adhaar_card)
            profile.address = job.get("address", profile.address)

            profile.landmark = job.get("landmark", profile.landmark)
            profile.city = job.get("city", profile.city)
            profile.state = job.get("state", profile.state)
            profile.country = job.get("country", profile.country)
            profile.pincode = job.get("pincode", profile.pincode)
            profile.is_verified = job.get("is_verified", profile.is_verified)
            profile.is_vehicle = job.get("is_vehicle", profile.is_vehicle)
            profile.is_delivery_boy = job.get(
                "is_delivery_boy", profile.is_delivery_boy
            )
            profile.is_permanent_employee = job.get(
                "is_permanent_employee", profile.is_permanent_employee
            )
            profile.is_freelancer = job.get("is_freelancer", profile.is_freelancer)
            profile.save()

        if files is not None:
            for f in files:
                fl = files_data.pop(0)
                fl.file_type = f.get("file_type", fl.file_type)
                fl.label = f.get("label", fl.label)
                fl.file_url = f.get("file_url", fl.file_url)
                fl.save()

        if specifications is not None:
            for f in specifications:
                fl = specifications_data.pop(0)
                fl.spec_type = f.get("spec_type", fl.spec_type)
                fl.label = f.get("label", fl.label)
                fl.description = f.get("description", fl.description)
                fl.save()

        if skills is not None:
            for f in skills:
                fl = skills_data.pop(0)
                fl.level = f.get("level", fl.level)
                fl.label = f.get("label", fl.label)
                fl.description = f.get("description", fl.description)
                fl.save()

        if experiences is not None:
            for f in experiences:
                fl = experiences_data.pop(0)
                fl.title = f.get("title", fl.level)
                fl.organization = f.get("organization", fl.organization)
                fl.location = f.get("location", fl.location)
                fl.start_date = f.get("start_date", fl.start_date)
                fl.end_date = f.get("end_date", fl.end_date)
                fl.description = f.get("description", fl.description)
                fl.save()

        if educations is not None:
            for f in educations:
                fl = educations_data.pop(0)
                fl.title = f.get("title", fl.level)
                fl.specialization = f.get("specialization", fl.specialization)
                fl.organization = f.get("organization", fl.organization)
                fl.location = f.get("location", fl.location)
                fl.start_date = f.get("start_date", fl.start_date)
                fl.end_date = f.get("end_date", fl.end_date)
                fl.description = f.get("description", fl.description)
                fl.save()

        return instance


class PermanentEmployeeCreateSerializer(serializers.ModelSerializer):
    specifications = PermanentEmployeeSpecificationSerializer(many=True, required=False)
    files = PermanentEmployeeFileSerializer(many=True, required=False)
    educations = PermanentEmployeeEducationSerializer(many=True, required=False)
    skills = PermanentEmployeeSkillSerializer(many=True, required=False)
    experiences = PermanentEmployeeExperienceSerializer(many=True, required=False)

    class Meta:
        model = PermanentEmployee
        fields = [
            "id",
            "job_profile",
            "is_recharged",
            "active",
            "added",
            "updated",
            "short_bio",
            "files",
            "specifications",
            "educations",
            "skills",
            "experiences",
        ]

    def create(self, validated_data):
        job_profile = validated_data.get("job_profile")
        profile = JobProfile.objects.filter(id=job_profile).first()

        files = validated_data.pop("files", None)
        specifications = validated_data.pop("specifications", None)
        educations = validated_data.pop("educations", None)
        skills = validated_data.pop("skills", None)
        experiences = validated_data.pop("experiences", None)
        if profile.is_permanent_employee:
            try:
                permanent_employee = PermanentEmployee.objects.get(job_profile=profile)
            except PermanentEmployee.DoesNotExist:
                profile.is_permanent_employee = True
                profile.save()
                permanent_employee = PermanentEmployee.objects.create(**validated_data)
        else:
            profile.is_permanent_employee = True
            profile.save()
            permanent_employee = PermanentEmployee.objects.create(**validated_data)

        if files is not None:
            for f in files:
                PermanentEmployeeFile.objects.create(
                    **f, permanent_employee=permanent_employee
                )

        if specifications is not None:
            for f in specifications:
                PermanentEmployeeSpecification.objects.create(
                    **f, permanent_employee=permanent_employee
                )

        if skills is not None:
            for f in skills:
                PermanentEmployeeSkill.objects.create(
                    **f, permanent_employee=permanent_employee
                )

        if educations is not None:
            for f in educations:
                PermanentEmployeeEducation.objects.create(
                    **f, permanent_employee=permanent_employee
                )

        if experiences is not None:
            for f in experiences:
                PermanentEmployeeExperience.objects.create(
                    **f, permanent_employee=permanent_employee
                )
        return permanent_employee


class FreelancerSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreelancerSpecification
        fields = ["id", "spec_type", "label", "description", "added"]


class FreelancerSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreelancerSkill
        fields = ["id", "level", "label", "description", "added"]


class FreelancerExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreelancerExperience
        fields = [
            "id",
            "title",
            "organization",
            "location",
            "start_date",
            "end_date",
            "description",
            "added",
        ]


class FreelancerEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreelancerEducation
        fields = [
            "id",
            "title",
            "specialization",
            "organization",
            "location",
            "start_date",
            "end_date",
            "description",
            "added",
        ]


class FreelancerFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreelancerFile
        fields = ["id", "file_type", "label", "file_url", "added"]


class FreelancerShowSerializer(serializers.ModelSerializer):
    job_profile = JobProfileSerializer()
    specifications = FreelancerSpecificationSerializer(many=True)
    files = FreelancerFileSerializer(many=True)
    educations = FreelancerEducationSerializer(many=True)
    skills = FreelancerSkillSerializer(many=True)
    experiences = FreelancerExperienceSerializer(many=True)

    class Meta:
        model = Freelancer
        fields = [
            "id",
            "job_profile",
            "is_recharged",
            "active",
            "added",
            "updated",
            "short_bio",
            "files",
            "specifications",
            "educations",
            "skills",
            "experiences",
        ]

    def update(self, instance, validated_data):
        job = validated_data.pop("job_profile", None)
        files = validated_data.pop("files", None)
        specifications = validated_data.pop("specifications", None)
        profile = instance.job_profile

        files_data = (instance.files).all()
        files_data = list(files_data)
        specifications_data = (instance.specifications).all()
        specifications_data = list(specifications_data)

        skills_data = (instance.skills).all()
        skills_data = list(skills_data)

        educations_data = (instance.educations).all()
        educations_data = list(educations_data)

        experiences_data = (instance.experiences).all()
        experiences_data = list(experiences_data)

        instance.is_recharged = validated_data.get(
            "is_recharged", instance.is_recharged
        )
        instance.short_bio = validated_data.get("short_bio", instance.short_bio)
        instance.save()

        if job is not None:
            profile.alt_email = job.get("alt_email", profile.alt_email)
            profile.alt_phone_number = job.get(
                "alt_phone_number", profile.alt_phone_number
            )
            profile.photo_url = job.get("photo_url", profile.photo_url)
            profile.adhaar_card = job.get("adhaar_card", profile.adhaar_card)
            profile.address = job.get("address", profile.address)

            profile.landmark = job.get("landmark", profile.landmark)
            profile.city = job.get("city", profile.city)
            profile.state = job.get("state", profile.state)
            profile.country = job.get("country", profile.country)
            profile.pincode = job.get("pincode", profile.pincode)
            profile.is_verified = job.get("is_verified", profile.is_verified)
            profile.is_vehicle = job.get("is_vehicle", profile.is_vehicle)
            profile.is_delivery_boy = job.get(
                "is_delivery_boy", profile.is_delivery_boy
            )
            profile.is_permanent_employee = job.get(
                "is_permanent_employee", profile.is_permanent_employee
            )
            profile.is_freelancer = job.get("is_freelancer", profile.is_freelancer)
            profile.save()

        if files is not None:
            for f in files:
                fl = files_data.pop(0)
                fl.file_type = f.get("file_type", fl.file_type)
                fl.label = f.get("label", fl.label)
                fl.file_url = f.get("file_url", fl.file_url)
                fl.save()

        if specifications is not None:
            for f in specifications:
                fl = specifications_data.pop(0)
                fl.spec_type = f.get("spec_type", fl.spec_type)
                fl.label = f.get("label", fl.label)
                fl.description = f.get("description", fl.description)
                fl.save()

        if skills is not None:
            for f in skills:
                fl = skills_data.pop(0)
                fl.level = f.get("level", fl.level)
                fl.label = f.get("label", fl.label)
                fl.description = f.get("description", fl.description)
                fl.save()

        if experiences is not None:
            for f in experiences:
                fl = experiences_data.pop(0)
                fl.title = f.get("title", fl.level)
                fl.organization = f.get("organization", fl.organization)
                fl.location = f.get("location", fl.location)
                fl.start_date = f.get("start_date", fl.start_date)
                fl.end_date = f.get("end_date", fl.end_date)
                fl.description = f.get("description", fl.description)
                fl.save()

        if educations is not None:
            for f in educations:
                fl = educations_data.pop(0)
                fl.title = f.get("title", fl.level)
                fl.specialization = f.get("specialization", fl.specialization)
                fl.organization = f.get("organization", fl.organization)
                fl.location = f.get("location", fl.location)
                fl.start_date = f.get("start_date", fl.start_date)
                fl.end_date = f.get("end_date", fl.end_date)
                fl.description = f.get("description", fl.description)
                fl.save()

        return instance


class FreelancerCreateSerializer(serializers.ModelSerializer):
    specifications = FreelancerSpecificationSerializer(many=True, required=False)
    files = FreelancerFileSerializer(many=True, required=False)
    educations = FreelancerEducationSerializer(many=True, required=False)
    skills = FreelancerSkillSerializer(many=True, required=False)
    experiences = FreelancerExperienceSerializer(many=True, required=False)

    class Meta:
        model = Freelancer
        fields = [
            "id",
            "job_profile",
            "is_recharged",
            "active",
            "added",
            "updated",
            "short_bio",
            "files",
            "specifications",
            "educations",
            "skills",
            "experiences",
        ]

    def create(self, validated_data):
        job_profile = validated_data.get("job_profile")
        profile = JobProfile.objects.filter(id=job_profile).first()
        files = validated_data.pop("files", None)
        specifications = validated_data.pop("specifications", None)
        skills = validated_data.pop("skills", None)
        educations = validated_data.pop("educations", None)
        experiences = validated_data.pop("experiences", None)

        if profile.is_freelancer:
            try:
                freelancer = Freelancer.objects.get(job_profile=profile)
            except Freelancer.DoesNotExist:
                profile.is_freelancer = True
                profile.save()
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

        if skills is not None:
            for f in skills:
                FreelancerSkill.objects.create(
                    **f, permanent_employee=permanent_employee
                )

        if educations is not None:
            for f in educations:
                FreelancerEducation.objects.create(
                    **f, permanent_employee=permanent_employee
                )

        if experiences is not None:
            for f in experiences:
                FreelancerExperience.objects.create(
                    **f, permanent_employee=permanent_employee
                )
        return freelancer