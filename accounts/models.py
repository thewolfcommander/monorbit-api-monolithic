import random
from datetime import datetime, timedelta
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.core.validators import EmailValidator
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from monorbit.utils import tools, validators
from monorbit.utils.data.languages import LANGUAGES

import logging
logger = logging.getLogger(__name__)

def expiration_delta():
    return timezone.now() + timezone.timedelta(minutes=10)


class CustomUserManager(BaseUserManager):
    """
    This manager is for handling user authentication model and functioning
    """
    def create_user(self, email, mobile_number, full_name, password, **extra_fields):
        """
        This function will create the normal user. It will act as a helper function for creating super users.
        """
        user = self.model(mobile_number=mobile_number, email=email, full_name=full_name, *extra_fields)
        user.set_password(password)
        string = "MONO{}".format(str(mobile_number))
        user.hash_token = tools.label_gen(string)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, mobile_number, full_name, password, **extra_fields):
        """
        This function will create super user 
        """
        user = self.create_user(email, mobile_number, full_name, password, **extra_fields)
        user.is_admin=True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, mobile_number):
        """
        This function will set the username of the user to the mobile number
        """
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
    id = models.CharField(max_length=20, blank=True, unique=True, primary_key=True, help_text="Primary Key of the user model")
    hash_token = models.CharField(max_length=255, null=True, blank=True, help_text="This is long unique token that will be used for advanced purposes like app level authentication, etc.")
    full_name = models.CharField(max_length=255, null=True, blank=True, help_text="This will be the user's full name", verbose_name="full_name")
    email = models.EmailField(
        max_length=255, 
        validators=[EmailValidator, validators.custom_email_validator], 
        help_text="This will be the user's primary email",
        null=True,
        blank=True,
    )
    country_code = models.IntegerField(default=91, null=True, blank=True, help_text="This will be the country code of the user from which he/she is accessing the monorbit")
    mobile_number = models.CharField(unique=True, max_length=10, blank=True, help_text="This will be the user phone number", error_messages={'required': 'Please provide your mobile number.', 'unique': 'An account with this mobile number exist.', 'invalid': 'Mobile number should be valid'})
    gender = models.CharField(max_length=30, null=True, blank=True, choices=GENDER_CHOICES, default='Male', help_text="This will be the gender of the user - Choices are predefined above and should be changed only in accounts/models.py")
    dob = models.CharField(max_length=100, null=True, blank=True, default="22-01-2000", help_text="This would be the Date of birth of the user in the format - DD-MM-YYYY")
    registration_reference = models.CharField(max_length=255, null=True, blank=True, default="None", help_text="This would be the registration reference from which user have joined Monorbit")    
    city = models.CharField(max_length=255, null=True, blank=True, help_text="User's city of current residence")
    pincode = models.CharField(max_length=10, null=True, blank=True, help_text="User's Locality postal code of current residence")
    network_created = models.IntegerField(default=0, null=True, blank=True, help_text="It is the number of total network created by the user")
    otp_sent = models.IntegerField(default=0, null=True, blank=True, help_text="It the total number of OTP Sent to user in order to verify his/her phone number.")
    password_otp_sent = models.IntegerField(default=0, null=True, blank=True, help_text="It is the total number of password reset OTP sent to the user in case the user forgot his/her password")
    order_count = models.PositiveIntegerField(default=0, null=True, blank=True, help_text="It the total number of orders placed by the user on Monorbit Ecommerce")
    followed_networks = models.PositiveIntegerField(default=0, null=True, blank=True, help_text="It is the total number of networks a user joined to")
    
    # Different Flags
    is_consumer = models.BooleanField(default=True, help_text="This will determine whether the user is a consumer")
    is_creator = models.BooleanField(default=False, help_text="This will determine whether the user is a creator or business. Default it will be false")
    is_working_profile = models.BooleanField(default=False, help_text="This will determine whether the user has a working profile. Default it will be false")
    is_active = models.BooleanField(default=True, help_text="This will determine whether the user account is active or not")
    is_agreed_to_terms = models.BooleanField(default=True, help_text="This will determine whether the user is agreed to terms or not")
    is_admin = models.BooleanField(default=False, help_text="This will determine is the user is a super user or not")
    is_mobile_verified = models.BooleanField(default=False, help_text="This will determine whether the mobile number is verified or not")
    is_email_verified = models.BooleanField(default=False, help_text="This will determine whether the email address is verified or not")
    is_logged_in = models.BooleanField(default=False, help_text="This will determine whether the user is logged in or not.")
    is_archived = models.BooleanField(default=False, help_text="This will determine whether the user have deleted his/her account or not.")

    # Different Date Related Fields
    registered_on = models.DateTimeField(default=timezone.now, help_text="This will determine when the user registered")
    last_logged_in_time = models.DateTimeField(default=timezone.now, help_text="This will determine when the user logged in last time")
    updated_on = models.DateTimeField(auto_now=True, help_text="This will determine when the user updated his/her account details")


    # This object will connect this model to its manager
    objects = CustomUserManager()

    # Setting up the default username field of the user model
    USERNAME_FIELD = 'mobile_number'

    # Setting up the unique together fields for the user model
    UNIQUE_TOGETHER = ['mobile_number', 'email']

    # Setting up the required fields for the user model
    REQUIRED_FIELDS = ['email', 'full_name']

    def __str__(self):
        """
        This function is for better representation purposes of the model refernces
        """
        return "{}-{}".format(str(self.id), str(self.mobile_number))
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def localization(self):
        """
        This method will return all the localization references of the user. Useful in serializers/nested serializers
        """
        return self.userlocalization_set.all()

    
def first_time_user_initializers(sender, instance, **kwargs):
    """
    Signal Reciever for setting up important details about user before actually creating the user
    """
    if not instance.hash_token:
        # Creating the unique hash token in the format - MONO + 10 digit mobile number + Current Timestamp at which user is created
        string = "MONO{}".format(str(instance.mobile_number))
        instance.hash_token = tools.label_gen(string)
    
    if not instance.id:
        # Setting up the primary key of the user - Random 14 digits string of alphanumberic characters
        instance.id = tools.random_string_generator(14)

# Connecting the signal reciever to the signal sender
pre_save.connect(first_time_user_initializers, sender=User)


class PasswordResetToken(models.Model):
    """
    This model will keep records for the OTP Sent to user if they forgotten their password
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="This is the user reference who is requesting the OTP")
    token = models.CharField(max_length=10, null=True, blank=True, help_text="This is the OTP Sent to the user")
    created = models.DateTimeField(auto_now_add=True, help_text="This is the timestamp at which OTP is created")

    def __str__(self):
        return "{}-{}".format(str(self.user.mobile_number), str(self.token))


class EmailVerifyOTP(models.Model):
    """
    This model will keep records for the OTP Sent to the user in order to verify their email address or mobile number
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="This is the user reference who is requesting the OTP")
    otp = models.CharField(max_length=10, null=True, blank=True, help_text="This is the OTP Sent to the user")
    created = models.DateTimeField(auto_now_add=True, help_text="This is the timestamp at which OTP is created")

    def __str__(self):
        return "{}-{}".format(str(self.user.mobile_number), str(self.otp))


class PasswordUpdateToken(models.Model):
    """
    This model is deprecated and soon will be removed
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class UserLocalization(models.Model):
    """
    This model will keep track of the user's localization information
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="This is the user's reference to which localization is setting up")
    communication_language_code = models.CharField(max_length=5, null=True, blank=True, choices=LANGUAGES, default='en', help_text="This is the language used by user for communication purposes like chat, calls, support, etc.")
    interface_language_code = models.CharField(max_length=5, null=True, blank=True, choices=LANGUAGES, default='en', help_text="This is the language that user can set in order how he want to view the application")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="Timestamp at which localization is created")
    updated = models.DateTimeField(auto_now=True, help_text="Timestamp at which localization is updated")

    def __str__(self):
        return str(self.id)



def password_reset_token_reciever(sender, instance, **kwargs):
    """
    This signal reciever will generate the OTP for password reset
    """
    instance.token = tools.random_number_generator(1111, 9999)

def email_verify_otp_reciever(sender, instance, **kwargs):
    """
    This signal reciever will generate OTP for mobile and email verification
    """
    instance.otp = tools.random_number_generator(1111, 9999)

def password_update_token_reciever(sender, instance, **kwargs):
    instance.token = tools.random_string_generator(25)


# Connecting senders to recievers for signals
pre_save.connect(password_reset_token_reciever, sender=PasswordResetToken)
pre_save.connect(email_verify_otp_reciever, sender=EmailVerifyOTP)
pre_save.connect(password_update_token_reciever, sender=PasswordUpdateToken)
