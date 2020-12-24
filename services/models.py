from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save

from monorbit.utils import tools
from accounts.models import User
from network.models import Network

import logging
logger = logging.getLogger(__name__)



class ServiceCategory(models.Model):
    id = models.CharField(max_length=20,primary_key=True,unique=True,blank=True)
    name = models.CharField(max_length=255,blank=True,null=True)
    image = models.CharField(max_length=512,null=True,blank=True,default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg')
    created = models.DateTimeField(auto_now_add=True)
    network = models.ForeignKey(Network,on_delete=models.CASCADE,related_name='network')

    def __str__(self):
        return str(self.id)


class ServiceSubCategory(models.Model):
    id = models.CharField(max_length=20,primary_key=True,unique=True,blank=True)
    name = models.CharField(max_length=255,blank=True,null=True)
    service_category = models.ForeignKey(ServiceCategory,on_delete=models.CASCADE,related_name='service_category')
    image = models.CharField(max_length=512,blank=True,null=True,default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class Service(models.Model):
    id = models.CharField(max_length=20,primary_key=True,unique=True,blank=True)
    service_code = models.CharField(max_length=55,blank=True,null=True)
    name = models.CharField(max_length=255,blank=True,null=True)
    slug = models.CharField(max_length=255,blank=True,null=True)
    thumbnail_image = models.CharField(max_length=512,blank=True,null=True,default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg')
    mrp = models.DecimalField(default=0.00,max_digits=12,decimal_places=2,help_text="This would be Maximum Retail Price")
    nsp = models.DecimalField(default=0.00,max_digits=12,decimal_places=2,help_text="Net Selling Price - The price at which they offer")
    discount_percent = models.DecimalField(default=0.00, max_digits=12, decimal_places=2, help_text="dp = nsp/mrp * 100")
    tax = models.DecimalField(default=0.00,max_digits=12,decimal_places=2,help_text="Tax on the Service")
    chargeable_rate_period = models.CharField(max_length=125,blank=True,null=True)
    short_description = models.TextField(null=True,blank=True)
    rating = models.DecimalField(default=5.0,max_digits=2,decimal_places=1)
    no_of_reviews = models.IntegerField(null=True,blank=True,default=0)
    network = models.ForeignKey(Network,on_delete=models.CASCADE,related_name='network')
    service_category = models.ForeignKey(ServiceCategory,on_delete=models.CASCADE,related_name='service_category')
    service_sub_category = models.ForeignKey(ServiceSubCategory,on_delete=models.CASCADE,related_name='service_sub_category')
    is_available = models.BooleanField(default=True,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    is_refundable = models.BooleanField(default=False, null=True, blank=True, help_text="Is the current service is refundable?")
    is_returnable = models.BooleanField(default=False, null=True, blank=True, help_text="Is the current service is returnable?")
    is_active = models.BooleanField(default=True)
    is_archived = models.BooleanField(default=False)
    is_open_for_sharing = models.BooleanField(default=False)
    is_digital = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def images(self):
        return self.servicecallingimage_set.all()

    @property
    def videos(self):
        return self.servicecallingvideo_set.all()

    @property
    def documents(self):
        return self.servicecallingdocument_set.all()       


class ServiceCallingImage(models.Model):
    id = models.CharField(max_length=10,primary_key=True,unique=True,blank=True)
    service = models.ForeignKey(Service,on_delete=models.CASCADE)
    label = models.CharField(max_length=255,null=True,blank=True)
    image = models.URLField(null=True,blank=True,default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class ServiceCallingVideo(models.Model):
    id = models.CharField(max_length=10,primary_key=True,unique=True,blank=True)
    service = models.ForeignKey(Service,on_delete=models.CASCADE)
    label = models.CharField(max_length=255,null=True,blank=True)
    video = models.URLField(null=True,blank=True,default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

class ServiceCallingDocument(models.Model):
    id = models.CharField(max_length=10,primary_key=True,unique=True,blank=True)
    service = models.ForeignKey(Service,on_delete=models.CASCADE)
    label = models.CharField(max_length=255,null=True,blank=True)
    doc = models.URLField(null=True,blank=True,default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class ServiceReview(models.Model):
    id = models.CharField(max_length=10,primary_key=True,unique=True,blank=True)
    service = models.ForeignKey(Service,on_delete=models.CASCADE)
    by = models.ForeignKey(User,on_delete=models.CASCADE)
    rating = models.DecimalField(default=5.0, max_digits=2, decimal_places=1)
    comment = models.TextField(null=True, blank=True)
    is_spam = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)


def instance_id_generator(sender, instance, **kwargs):
    if not instance.id:
        instance.id = tools.random_string_generator(9).upper()

def image_label_generator(sender, instance, **kwargs):
    if not instance.label:
        instance.label = tools.label_gen("IMG-{}".format(str(instance.service.name)))

def video_label_generator(sender, instance, **kwargs):
    if not instance.label:
        instance.label = tools.label_gen("VID-{}".format(str(instance.service.name)))

def document_label_generator(sender, instance, **kwargs):
    if not instance.label:
        instance.label = tools.label_gen("DOC-{}".format(str(instance.service.name)))

    
def product_datainit_generator(sender, instance, **kwargs):
    instance.slug = tools.unique_slug_generator(instance)
    if not instance.service_code:
        instance.service_code = tools.label_gen(instance.network.id)
    instance.discount_percent = ((float(instance.mrp)-float(instance.nsp))/float(instance.mrp))*100


pre_save.connect(instance_id_generator, sender=ServiceCategory)
pre_save.connect(instance_id_generator, sender=ServiceSubCategory)
pre_save.connect(instance_id_generator, sender=Service)
pre_save.connect(instance_id_generator, sender=ServiceCallingImage)
pre_save.connect(instance_id_generator, sender=ServiceCallingVideo)
pre_save.connect(instance_id_generator, sender=ServiceCallingDocument)
pre_save.connect(instance_id_generator, sender=ServiceReview)

pre_save.connect(product_datainit_generator, sender=Service)
pre_save.connect(image_label_generator, sender=ServiceCallingImage)
pre_save.connect(video_label_generator, sender=ServiceCallingVideo)
pre_save.connect(document_label_generator, sender=ServiceCallingDocument)