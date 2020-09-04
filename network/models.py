from django.core.validators import EmailValidator, RegexValidator
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from accounts import models as acc_models
from monorbit.utils import tools, validators

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

import logging
logger = logging.getLogger(__name__)

# Create your models here.

class NetworkCategory(models.Model):
    """
    This is the category for which a network belongs to
    """
    name = models.CharField(max_length=255, null=True, blank=True)
    priority = models.IntegerField(default=2, null=True, blank=True)
    image = models.URLField(null=True, blank=True, default="https://content.monorbit.com/images/placeholder.png")
    created = models.DateTimeField(default=timezone.now)


class NetworkType(models.Model):
    """
    This is the category for which a network belongs to
    """
    name = models.CharField(max_length=255, null=True, blank=True)
    image = models.URLField(null=True, blank=True, default="https://content.monorbit.com/images/placeholder.png")
    created = models.DateTimeField(default=timezone.now)


# class NetworkSubCategory(models.Model):
#     """
#     This is the category for which a network belongs to
#     """
#     name = models.CharField(max_length=255, null=True, blank=True)
#     created = models.DateTimeField(default=timezone.now)


class Network(models.Model):
    """
    This is the base network which a business have to create. Inside this network, varioud store comes
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    urlid = models.CharField(max_length=255, unique=True, blank=True)
    user = models.ForeignKey(acc_models.User, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(NetworkCategory, on_delete=models.CASCADE, null=True, blank=True)
    network_type = models.ForeignKey(NetworkType, on_delete=models.CASCADE, null=True, blank=True)
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
    registered_stores = models.IntegerField(null=True, blank=True, default=1)
    
    # Documents Details
    gst = models.CharField(max_length=255, null=True, blank=True)
    adhaar = models.CharField(max_length=255, null=True, blank=True)
    pan = models.CharField(max_length=255, null=True, blank=True)

    # Flags
    is_verified = models.BooleanField(default=False, help_text="This is for verification of uploaded documents")
    is_active = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    is_spam = models.BooleanField(default=False)
    is_video = models.BooleanField(default=False)
    is_document = models.BooleanField(default=False)

    # Time related fields
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    @property
    def images(self):
        return self.networkimage_set.all()

    @property
    def videos(self):
        return self.networkvideo_set.all()

    @property
    def documents(self):
        return self.networkdocument_set.all()

    @property
    def timings(self):
        return self.networkoperationtiming_set.all()

    @property
    def locations(self):
        return self.networkoperationlocation_set.all()

    
class NetworkImage(models.Model):
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    label = models.CharField(max_length=255, null=True, blank=True)
    image = models.URLField(null=True, blank=True)

    def __str__(self):
        return str(self.id)


class NetworkVideo(models.Model):
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    label = models.CharField(max_length=255, null=True, blank=True)
    video = models.URLField(null=True, blank=True)

    def __str__(self):
        return str(self.id)


class NetworkDocument(models.Model):
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    label = models.CharField(max_length=255, null=True, blank=True)
    doc = models.URLField(null=True, blank=True)

    def __str__(self):
        return str(self.id)


class NetworkOperationTiming(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
        ('All', 'All'),
        ('Weekday', 'Weekday'),
        ('Weekend', 'Weekend'),
    ]
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    day = models.CharField(max_length=255, null=True, blank=True)
    opening = models.CharField(max_length=25, null=True, blank=True)
    status = models.BooleanField(default=True)
    closing = models.CharField(max_length=25, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class NetworkOperationLocation(models.Model):
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    pincode = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class NetworkReview(models.Model):
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    by = models.ForeignKey(acc_models.User, on_delete=models.CASCADE)
    rating = models.DecimalField(default=5.0, max_digits=2, decimal_places=1)
    comment = models.TextField(null=True, blank=True)
    is_spam = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)


    
def instance_id_generator(sender, instance, **kwargs):
    if not instance.id:
        instance.id = tools.random_string_generator(8).upper()


def image_label_generator(sender, instance, **kwargs):
    if not instance.label:
        instance.label = tools.label_gen("IMG")

def video_label_generator(sender, instance, **kwargs):
    if not instance.label:
        instance.label = tools.label_gen("VID")

def document_label_generator(sender, instance, **kwargs):
    if not instance.label:
        instance.label = tools.label_gen("DOC")

    
def network_url_id_generator(sender, instance, **kwargs):
    if not instance.urlid:
        instance.urlid = tools.short_url_id_gen()
        print("A network created having URL ID - {}".format(instance.urlid))


pre_save.connect(instance_id_generator, sender=Network)
pre_save.connect(network_url_id_generator, sender=Network)
pre_save.connect(instance_id_generator, sender=NetworkImage)
pre_save.connect(instance_id_generator, sender=NetworkVideo)
pre_save.connect(instance_id_generator, sender=NetworkDocument)
pre_save.connect(instance_id_generator, sender=NetworkOperationLocation)
pre_save.connect(instance_id_generator, sender=NetworkOperationTiming)
pre_save.connect(instance_id_generator, sender=NetworkReview)

pre_save.connect(image_label_generator, sender=NetworkImage)
pre_save.connect(video_label_generator, sender=NetworkVideo)
pre_save.connect(document_label_generator, sender=NetworkDocument)