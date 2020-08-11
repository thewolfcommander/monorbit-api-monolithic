import random
import uuid
from datetime import datetime, timedelta
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.core.validators import EmailValidator, RegexValidator
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from monorbit.utils import tools, validators



class CustomUserManager(BaseUserManager):
    """
    This manager is for handling user authentication model and functioning
    """
    def create_user(self, email, mobile_number, password, **extra_fields):

        user = self.model(mobile_number=mobile_number, email=email, *extra_fields)
        user.set_password(password)
        string = "MONO{}".format(str(mobile_number))
        user.hash_token = tools.label_gen(string)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, mobile_number, password, **extra_fields):
        user = self.create_user(email, mobile_number, password, **extra_fields)
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
    )
    country_code = models.IntegerField(default=91, null=True, blank=True)
    mobile_number = models.CharField(unique=True, primary_key=True, max_length=10, blank=True, help_text="This will be the user phone number", error_messages={'required': 'Please provide your mobile number.', 'unique': 'An account with this mobile number exist.', 'invalid': 'Mobile number should be valid'})
    gender = models.CharField(max_length=30, null=True, blank=True, choices=GENDER_CHOICES, default='Male')
    dob = models.CharField(max_length=100, null=True, blank=True, default="22-01-2000")
    registration_reference = models.CharField(max_length=255, null=True, blank=True, default="None")    
    city = models.CharField(max_length=255, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    network_created = models.IntegerField(default=0, null=True, blank=True)
    otp_sent = models.IntegerField(default=0, null=True, blank=True)
    
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
        string = "MONO{}".format(str(instance.mobile_number))
        instance.token = tools.label_gen(string)

    
pre_save.connect(first_time_user_initializers, sender=User)



class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=10, null=True, blank=True)
    expiry = models.DateTimeField(default=datetime.now()+timedelta(minutes=60), null=True, blank=True)
    created = models.DateTimeField(default=datetime.now(), null=True, blank=True)

    def __str__(self):
        return str(self.id)

class EmailVerifyOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=10, null=True, blank=True)
    expiry = models.DateTimeField(default=datetime.now()+timedelta(minutes=30), null=True, blank=True)
    created = models.DateTimeField(default=datetime.now(), null=True, blank=True)

    def __str__(self):
        return str(self.id)


class PasswordUpdateToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.id)


def password_reset_token_reciever(sender, instance, **kwargs):
    instance.token = tools.random_number_generator(111111, 999999)

def email_verify_otp_reciever(sender, instance, **kwargs):
    instance.otp = tools.random_number_generator(111111, 999999)

def password_update_token_reciever(sender, instance, **kwargs):
    instance.token = tools.random_string_generator(25)

pre_save.connect(password_reset_token_reciever, sender=PasswordResetToken)
pre_save.connect(email_verify_otp_reciever, sender=EmailVerifyOTP)
pre_save.connect(password_update_token_reciever, sender=PasswordUpdateToken)