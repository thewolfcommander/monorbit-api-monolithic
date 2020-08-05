from django.core.validators import EmailValidator, RegexValidator
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from accounts import models as acc_models
from network import models as net_models
from monorbit.utils import tools, validators

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")


class Store(models.Model):
    """
    Store represents the online legacy of shops or service portals that a network or business owner can make
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    network = models.ForeignKey(net_models.Network, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    thumbnail_image = models.URLField(null=True, blank=True, default="https://content.monorbit.com/images/placeholder.png")
    address = models.CharField(max_length=255, null=True, blank=True)
    landmark = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    alt_phone = models.CharField(validators=[phone_regex,], max_length=17, null=True, blank=True, help_text="This will be the Alternative phone number")
    alt_email = models.EmailField(
        max_length=255, 
        validators=[EmailValidator], 
        help_text="This will be the alternative email",
        null=True,
        blank=True,
    )
    rating = models.DecimalField(default=5.0, max_digits=2, decimal_places=1)
    no_of_reviews = models.IntegerField(null=True, blank=True, default=0)

    # Flags
    is_active = models.BooleanField(default=True)
    is_archived = models.BooleanField(default=False)
    is_default = models.BooleanField(default=True)

    # Time related fields
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


    
def instance_id_generator(sender, instance, **kwargs):
    if not instance.id:
        instance.id = tools.random_string_generator(12).upper()


pre_save.connect(instance_id_generator, sender=Store)