from django.db import models
from django.db.models.signals import pre_save
from django.db.models.aggregates import Count
from random import randint

from monorbit.utils import tools

from accounts.models import User
from network.models import Network
from orders.models import Order
# Create your models here.

class TipToGrowManager(models.Manager):
    def random(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]


class TipToGrow(models.Model):
    """
    This model will keep record of all the details about the tps that are going to show on network dashboard.
    """
    tip = models.TextField(null=True, blank=True)
    upvotes = models.IntegerField(default=0, null=True, blank=True)
    downvotes = models.IntegerField(default=0, null=True, blank=True)
    active = models.BooleanField(default=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = TipToGrowManager()

    def __str__(self):
        return str(self.id)

    
class EmailSentToUsers(models.Model):
    EMAIL_TYPE = [
        ('greeting', 'Greeting'),
        ('transaction', 'Transaction'),
        ('bug_report', 'Bug Report'),
        ('promotion', 'Promotion'),
        ('verification', 'Verification'),
        ('security', 'Security'),
    ]
    email_type = models.CharField(max_length=255, null=True, blank=True)
    sent_from_ip_address = models.GenericIPAddressField(null=True, blank=True)
    email_sent_to = models.EmailField(null=True, blank=True)
    email_sent_from = models.EmailField(null=True, blank=True)
    subject = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    sent_on = models.DateTimeField(auto_now_add=True)
    is_success = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)


class UserLoginActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    os_platform = models.CharField(max_length=255, null=True, blank=True)
    browser = models.CharField(max_length=255, null=True, blank=True)
    is_logged_from_mobile = models.BooleanField(default=False)
    is_logged_from_web = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    
class ActionsActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=50, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    os_platform = models.CharField(max_length=255, null=True, blank=True)
    api_url = models.URLField(null=True, blank=True)
    status_code = models.IntegerField(default=200, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    
class UserDeviceRegistration(models.Model):
    id = models.CharField(max_length=128, unique=True, blank=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_type = models.CharField(max_length=255, null=True, blank=True)
    operating_system = models.CharField(max_length=255, null=True, blank=True)
    browser = models.CharField(max_length=255, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    lat = models.CharField(max_length=50, null=True, blank=True)
    lng = models.CharField(max_length=50, null=True, blank=True)
    device_language = models.CharField(max_length=50, null=True, blank=True)
    user_agent = models.CharField(max_length=255, null=True, blank=True)
    is_app = models.BooleanField(default=False)
    is_browser = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class TempFile(models.Model):
    pass


class NetworkOrder(models.Model):
    network=models.ForeignKey(Network, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class NewsAndEvent(models.Model):
    CATEGORY = [
        ('news', 'News'),
        ('event', 'Event'),
        ('announcement', 'Announcement'),
        ('activity', 'Activity'),
        ('change_log', 'Change Logs'),
        ('feature_update', 'Feature Updates'),
        ('bug_fixes', 'Bug Fixes'),
        ('advertisement', 'Advertisement')
    ]
    category = models.CharField(max_length=255, null=True, blank=True, choices=CATEGORY, default='news')
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg')
    upvotes = models.IntegerField(default=0, null=True, blank=True)
    downvotes = models.IntegerField(default=0, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.id)


def id_initializer(sender, instance, **kwargs):
    if not instance.id:
        instance.id = tools.random_string_generator(56)

pre_save.connect(id_initializer, sender=UserDeviceRegistration)