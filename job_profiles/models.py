import datetime

from django.core.validators import EmailValidator, RegexValidator
from django.db import models
from django.db.models.signals import pre_save

from accounts.models import User
from monorbit.utils import tools, validators


import logging
logger = logging.getLogger(__name__)


class JobProfile(models.Model):
    """
    This will be the common model for all the job profiles viz. Delivery Boy, Permanent Job Profiles, and Freelancers. They all have to create a common job profile.
    """
    id  = models.CharField(max_length=50, primary_key=True, unique=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    alt_email = models.EmailField(
        max_length=255, 
        validators=[EmailValidator, validators.custom_email_validator], 
        help_text="This will be the user's alternative email",
        null=True, 
        blank=True
    )
    alt_phone_number = models.CharField(max_length=10, blank=True, null=True, help_text="This will be the user's alternative phone number")
    photo_url = models.URLField(null=True, blank=True, help_text="This will be applier's passport size photograph")
    adhaar_card = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True, help_text="Address Line 1")
    landmark = models.CharField(max_length=255, null=True, blank=True, help_text="Landmark")
    city = models.CharField(max_length=255, null=True, blank=True, help_text="City you are living in")
    state = models.CharField(max_length=255, null=True, blank=True, help_text="State you belong to")
    country = models.CharField(max_length=255, null=True, blank=True, help_text="Country")
    pincode = models.CharField(max_length=15, null=True, blank=True, help_text="Area POstal code")

    is_verified = models.BooleanField(default=False)
    is_vehicle = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_delivery_boy = models.BooleanField(default=False)
    is_permanent_employee = models.BooleanField(default=False)
    is_freelancer = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Job Profile"
        verbose_name_plural = "Job Profiles"

    
    def __str__(self):
        return str(self.id)



class CommonInfo(models.Model):
    """
    This will be the common info for the profiles.
    """
    id  = models.CharField(max_length=50, primary_key=True, unique=True, blank=True)
    job_profile = models.ForeignKey(JobProfile, on_delete=models.CASCADE)
    is_recharged = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)



class DeliveryBoy(CommonInfo):
    """
    This will be the delivery boy profile extending CommonInfo
    """
    short_bio = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Delivery Boy Profile"
        verbose_name_plural = "Delivery Boy Profiles"

    
    def __str__(self):
        return str(self.id)

    
    @property
    def vehicles(self):
        return self.deliveryboyvehicle_set.all()

    

class DeliveryBoyVehicle(models.Model):
    """
    If is_vehicle is True then this model will be activated
    """
    TYPE_OF_VEHICLE = [
        ('bicycle', 'Bi Cycle'),
        ('motor_bike', 'Motor Bike'),
        ('car', 'Car'),
        ('semi_truck', 'Semi Truck'),
        ('other', 'Other')
    ]

    id  = models.CharField(max_length=50, primary_key=True, unique=True, blank=True)
    delivery_boy = models.ForeignKey(DeliveryBoy, on_delete=models.CASCADE)
    driving_license = models.CharField(max_length=50, null=True, blank=True, help_text="Driving License of the Delivery Boy")
    type_of_vehicle = models.CharField(max_length=255, choices=TYPE_OF_VEHICLE, default="motor_bike")
    vehicle_license = models.CharField(max_length=50, unique=True, null=True, blank=True, help_text="Vehicle License Number")
    valid_upto = models.DateField(default=datetime.date.today, help_text="Validity date of Vehicle")
    vehicle_photo_url = models.URLField(blank=True, null=True, help_text="Upload Vehicle Image from front showing verhicle registration number. We will then verify the number from this image with vehicle_license field")
    active = models.BooleanField(default=False)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = "Delivery Boy Vehicle"
        verbose_name_plural = "Delivery Boy Vehicles"

    
    def __str__(self):
        return str(self.id)

    

class PermanentEmployee(CommonInfo):
    """
    This will be the Permanent Employee profile extending CommonInfo
    """
    short_bio = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Permanent Employee Profile"
        verbose_name_plural = "Permanent Employee Profiles"

    
    def __str__(self):
        return str(self.id)

    @property
    def files(self):
        return self.permanentemployeefile_set.all()

    @property
    def specifications(self):
        return self.permanentemployeespecification_set.all()

    
class PermanentEmployeeSpecification(models.Model):
    """
    These will be different dynamic fields for permanent employee profile
    """
    SPEC_TYPE = [
        ('skills', 'Skills'),
        ('link', 'Links'),
        ('experience', 'Experiences'),
        ('other', 'Other')
    ]
    id  = models.CharField(max_length=50, primary_key=True, unique=True, blank=True)
    permanent_employee = models.ForeignKey(PermanentEmployee, on_delete=models.CASCADE)
    spec_type = models.CharField(max_length=50, choices=SPEC_TYPE, default="skills")
    label = models.CharField(max_length=255, null=True, blank=True, help_text="Label of the Specification")
    description = models.TextField(null=True, blank=True, help_text="Description of the Specification")
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Permanent Employee Specification"
        verbose_name_plural = "Permanent Employee Specifications"

    
    def __str__(self):
        return str(self.id)

    

class PermanentEmployeeFile(models.Model):
    """
    These will be different dynamic files for permanent employee profile
    """
    FILE_TYPE = [
        ('document', 'Document'),
        ('image', 'Image'),
        ('video', 'Video')
    ]
    id  = models.CharField(max_length=50, primary_key=True, unique=True, blank=True)
    permanent_employee = models.ForeignKey(PermanentEmployee, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=50, choices=FILE_TYPE, default="image")
    label = models.CharField(max_length=255, null=True, blank=True, help_text="Label on the File")
    file_url = models.URLField(null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Permanent Employee File"
        verbose_name_plural = "Permanent Employee Files"

    
    def __str__(self):
        return str(self.id)



class Freelancer(CommonInfo):
    """
    This will be the Freelancer profile extending CommonInfo
    """
    short_bio = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Freelancer Profile"
        verbose_name_plural = "Freelancer Profiles"

    
    def __str__(self):
        return str(self.id)

    @property
    def files(self):
        return self.freelancerfile_set.all()

    @property
    def specifications(self):
        return self.freelancerspecification_set.all()

    
class FreelancerSpecification(models.Model):
    """
    These will be different dynamic fields for Freelancer profile
    """
    SPEC_TYPE = [
        ('skills', 'Skills'),
        ('link', 'Links'),
        ('experience', 'Experiences'),
        ('other', 'Other')
    ]
    id  = models.CharField(max_length=50, primary_key=True, unique=True, blank=True)
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    spec_type = models.CharField(max_length=50, choices=SPEC_TYPE, default="skills")
    label = models.CharField(max_length=255, null=True, blank=True, help_text="Label of the Specification")
    description = models.TextField(null=True, blank=True, help_text="Description of the Specification")
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Freelancer Specification"
        verbose_name_plural = "Freelancer Specifications"

    
    def __str__(self):
        return str(self.id)

    

class FreelancerFile(models.Model):
    """
    These will be different dynamic files for Freelancer profile
    """
    FILE_TYPE = [
        ('document', 'Document'),
        ('image', 'Image'),
        ('video', 'Video')
    ]
    id  = models.CharField(max_length=50, primary_key=True, unique=True, blank=True)
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=50, choices=FILE_TYPE, default="image")
    label = models.CharField(max_length=255, null=True, blank=True, help_text="Label on the File")
    file_url = models.URLField(null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Freelancer File"
        verbose_name_plural = "Freelancer Files"

    
    def __str__(self):
        return str(self.id)


    

def pre_save_id_receiver(sender, instance, **kwargs):
    if not instance.id:
        instance.id = tools.random_string_generator(9)

pre_save.connect(pre_save_id_receiver, sender=JobProfile)
pre_save.connect(pre_save_id_receiver, sender=DeliveryBoy)
pre_save.connect(pre_save_id_receiver, sender=DeliveryBoyVehicle)
pre_save.connect(pre_save_id_receiver, sender=PermanentEmployee)
pre_save.connect(pre_save_id_receiver, sender=PermanentEmployeeFile)
pre_save.connect(pre_save_id_receiver, sender=PermanentEmployeeSpecification)
pre_save.connect(pre_save_id_receiver, sender=Freelancer)
pre_save.connect(pre_save_id_receiver, sender=FreelancerFile)
pre_save.connect(pre_save_id_receiver, sender=FreelancerSpecification)