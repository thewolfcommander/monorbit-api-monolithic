import uuid

from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.core.validators import EmailValidator, RegexValidator
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from monorbit.utils import tools, validators

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")


class CustomUserManager(BaseUserManager):
    """
    This manager is for handling user authentication model and functioning
    """
    def create_user(self, email, mobile_number, password, **extra_fields):

        user = self.model(mobile_number=mobile_number, email=email, *extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, mobile_number, password, **extra_fields):
        user = self.create_user(email, mobile_number, password, **extra_fields)
        user.hash_token = tools.random_string_generator(112)
        user.is_admin=True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, mobile_number):
        return self.get(mobile_number=mobile_number)


class User(AbstractBaseUser, PermissionsMixin):
    """
    This model is for handling all the information related to the users on the platform. Morover the signup/signin process also going to be handled by this model
    """
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Transgender', 'Transgender'),
        ('Custom', 'Custom'),
    ]
    hash_token = models.CharField(max_length=255, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True, help_text="This will be the user full name", verbose_name="full_name")
    email = models.EmailField(
        max_length=255, 
        validators=[EmailValidator, validators.custom_email_validator], 
        help_text="This will be the user email",
        null=True,
        blank=True,
        error_messages={'required': 'Please provide your email address.', 'unique': 'An account with this email exist.'}
    )
    mobile_number = models.CharField(validators=[phone_regex,], unique=True, primary_key=True, max_length=17, blank=True, help_text="This will be the user phone number")
    gender = models.CharField(max_length=30, null=True, blank=True, choices=GENDER_CHOICES, default='Male')
    dob = models.CharField(max_length=100, null=True, blank=True, default="22-01-2000")
    registration_reference = models.CharField(max_length=255, null=True, blank=True, default="None")    
    city = models.CharField(max_length=255, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    network_created = models.IntegerField(default=0, null=True, blank=True)
    
    # Different Flags
    is_consumer = models.BooleanField(default=True, help_text="This will determine whether the user is a consumer")
    is_creator = models.BooleanField(default=False, help_text="This will determine whether the user is a creator. Default it will be false")
    is_working_profile = models.BooleanField(default=False, help_text="This will determine whether the user has a working profile. Default it will be false")
    is_active = models.BooleanField(default=True, help_text="This will determine whether the user accound is active or not")
    is_agreed_to_terms = models.BooleanField(default=True, help_text="This will determine whether the user is agreed to terms or not")
    is_admin = models.BooleanField(default=False)
    is_mobile_verified = models.BooleanField(default=False, help_text="This will determine whether the mobile number is verified or not")
    is_email_verified = models.BooleanField(default=False, help_text="This will determine whether the email address is verified or not")
    is_logged_in = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    # Different Date Related Fields
    registered_on = models.DateTimeField(default=timezone.now, help_text="This will determine when the user registered")
    last_logged_in_time = models.DateTimeField(default=timezone.now, help_text="This will determine when the user registered")
    updated_on = models.DateTimeField(auto_now=True, help_text="This will determine when the user updated")


    objects = CustomUserManager()

    USERNAME_FIELD = 'mobile_number'
    UNIQUE_TOGETHER = ['mobile_number', 'email']
    REQUIRED_FIELDS = ['email', 'full_name']

    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


    
def first_time_user_initializers(sender, instance, **kwargs):
    if not instance.hash_token:
        instance.token = tools.random_string_generator(112)

    
pre_save.connect(first_time_user_initializers, sender=User)
