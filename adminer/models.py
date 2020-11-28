from django.db import models
from django.db.models.signals import pre_save

from monorbit.utils import tools


class ContactUs(models.Model):
    """
    This model will keep record of the users that will contact us
    """
    id = models.CharField(max_length=25, blank=True, primary_key=True, unique=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    lat = models.CharField(max_length=50, null=True, blank=True)
    lng = models.CharField(max_length=50, null=True, blank=True)
    is_email = models.BooleanField(default=False)
    is_phone = models.BooleanField(default=False)
    is_contacted = models.BooleanField(default=False)
    is_business = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


def id_gen(sender, instance, **kwargs):
    if not instance.id:
        instance.id = tools.random_string_generator(size=6).upper()

pre_save.connect(id_gen, sender=ContactUs)