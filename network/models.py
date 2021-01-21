from django.core.validators import EmailValidator, RegexValidator
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils import timezone

from accounts import models as acc_models
# from orders.models import Order
from job_profiles.models import JobProfile
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
    image = models.URLField(null=True, blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg')
    created = models.DateTimeField(default=timezone.now)


class NetworkType(models.Model):
    """
    This is the category for which a network belongs to
    """
    name = models.CharField(max_length=255, null=True, blank=True)
    image = models.URLField(null=True, blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg')
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
    network_url = models.URLField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True, help_text="This field will tell about the personal comment about the network. Only for admin purpose.")
    user = models.ForeignKey(acc_models.User, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(NetworkCategory, on_delete=models.CASCADE, null=True, blank=True)
    network_type = models.ForeignKey(NetworkType, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    thumbnail_image = models.URLField(null=True, blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg')
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
    followers = models.PositiveIntegerField(null=True, blank=True, default=0)
    
    # Documents Details
    gst = models.CharField(max_length=255, null=True, blank=True)
    adhaar = models.CharField(max_length=255, null=True, blank=True)
    pan = models.CharField(max_length=255, null=True, blank=True)

    # Flags
    is_verified = models.BooleanField(default=False, help_text="This is for verification of uploaded documents")
    is_active = models.BooleanField(default=True)
    is_basic = models.BooleanField(default=True)
    is_economy = models.BooleanField(default=False)
    is_elite = models.BooleanField(default=False)
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

    @property
    def options(self):
        return self.networkoption


def network_option_update_receiver(sender, instance, **kwargs):
    """
    This receiver will update the network options every time the network saved
    """
    try:
        option = instance.networkoption
    except Exception as e:
        print("#### {}".format(str(e)))
        NetworkOption.objects.create(network=instance)

# pre_save.connect(network_option_update_receiver, sender=Network)

class NetworkOption(models.Model):
    """
    These will be special options for setting up network's better functionalities
    """
    network = models.OneToOneField(Network, on_delete=models.CASCADE)
    is_special_user = models.BooleanField(default=False, help_text="This field will tell whether the network is a special network on monorbit")
    is_backer = models.BooleanField(default=False, help_text="This field will tell whether the network is the backer or sponsor of Monorbit Platform")
    is_kyc = models.BooleanField(default=False, help_text="This field will tell whether the KYC of the network have been done or not")
    is_address_private = models.BooleanField(default=False, help_text="This field when true will keep the address of the network private.")
    is_phone_and_email_private = models.BooleanField(default=False, help_text="This field when true will keep the phone number and email of the network private")
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


    
class NetworkImage(models.Model):
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    label = models.CharField(max_length=255, null=True, blank=True)
    image = models.URLField(null=True, blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg')

    def __str__(self):
        return str(self.id)


class NetworkVideo(models.Model):
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    label = models.CharField(max_length=255, null=True, blank=True)
    video = models.URLField(null=True, blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg')

    def __str__(self):
        return str(self.id)


class NetworkDocument(models.Model):
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    label = models.CharField(max_length=255, null=True, blank=True)
    doc = models.URLField(null=True, blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg')

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
    day = models.CharField(max_length=255, null=True, blank=True, choices=DAY_CHOICES, default='All')
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

    
# class NetworkOrder(models.Model):
#     network = models.ForeignKey(Network, on_delete=models.CASCADE)
#     # order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     order = models.CharField(max_length=255, null=True, blank=True)
#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return str(self.id)


class NetworkJob(models.Model):
    """
    This model will keep record of all the jobs created by the network in which job profiles can apply
    """
    JOB_TYPE = [
        ('freelancer', 'Freelancer'),
        ('delivery', 'Delivery'),
        ('permanent', 'Permanent')
    ]
    SALARY_PAYOUT_TYPE = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('bimonthly', 'Bi Monthly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('biyearly', 'Bi Yearly'),
        ('yearly', 'Yearly'),
        ('work', 'Work Basis')
    ]
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    job_name = models.CharField(max_length=255, null=True, blank=True)
    job_type = models.CharField(max_length=255, null=True, blank=True, choices=JOB_TYPE, default="permanent")
    job_description = models.TextField(null=True, blank=True)
    job_requirements = models.TextField(null=True, blank=True)
    salary_payout_type = models.CharField(max_length=255, null=True, blank=True, choices=SALARY_PAYOUT_TYPE, default="monthly")
    salary_lower_range = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    salary_upper_range = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    actual_salary = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    age_bar_upper = models.IntegerField(default=45, null=True, blank=True)
    age_bar_lower = models.IntegerField(default=18, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_spam = models.BooleanField(default=False)
    is_vacant = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    
class NetworkStaff(models.Model):
    """
    This will be the staff of the network
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    job = models.ForeignKey(NetworkJob, on_delete=models.CASCADE)
    profile = models.ForeignKey(JobProfile, on_delete=models.CASCADE)
    application_id = models.CharField(max_length=20, null=True, blank=True)
    promoted_count = models.IntegerField(default=0)
    demoted_count = models.IntegerField(default=0)
    employee_score = models.IntegerField(default=10, help_text="This score would be given to employee out of 10.")
    is_active = models.BooleanField(default=True)
    joined = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id


class NetworkJobOffering(models.Model):
    """
    This model will hold the information about the job offerings for a particular network job. This is the model which will be used for application transactions
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    job = models.ForeignKey(NetworkJob, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    offering_information = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_filled = models.BooleanField(default=False)
    max_staff_for_job = models.IntegerField(default=5, null=True, blank=True)
    last_date = models.DateField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class NetworkStat(models.Model):
    """
    This model will keep the information about the stats of the networks
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    total_income = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    orders_recieved = models.IntegerField(default=0, null=True, blank=True)
    total_sales = models.IntegerField(default=0, null=True, blank=True, help_text="Total number of meaningful orders")
    refunds = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


def activity_expiry(days, date=timezone.now()):
    time = date + timezone.timedelta(days=days)
    return time


class NetworkTrial(models.Model):
    """
    This model will keep record of the trial period of the networks
    """
    APPLICABLE_OFFER = [
        ("republic", "Republic"),
        ("normal", "Normal")
    ]
    network = models.OneToOneField(Network, on_delete=models.CASCADE)
    applicable_offer = models.CharField(max_length=255, choices=APPLICABLE_OFFER, null=True, blank=True, default="normal")
    trial_days = models.IntegerField(default=30, null=True, blank=True)
    expiry = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


"""

USEFUL SIGNALS FOR ABOVE MODELS

"""


    
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
        instance.urlid = tools.username_generator(instance.name)
        print("A network created having Username - {}".format(instance.urlid))

    
def check_for_plan(sender, instance, **kwargs):
    if instance.is_elite:
        instance.is_economy = False
        instance.is_basic = False
    elif instance.is_economy:
        instance.is_elite = False
        instance.is_basic = False
    else:
        instance.is_basic = True
        instance.is_elite = False
        instance.is_basic = False

    try:
        trial = NetworkTrial.objects.get(network=instance)
    except NetworkTrial.DoesNotExist:
        trial = NetworkTrial.objects.create(network=instance, applicable_offer="republic", trial_days=90)
        trial.expiry = activity_expiry(trial.trial_days)
        trial.save()

    
def stat_create_receiver(sender, instance, **kwargs):
    try:
        NetworkStat.objects.get(network=instance)
    except NetworkStat.DoesNotExist:
        NetworkStat.objects.create(network=instance)


pre_save.connect(instance_id_generator, sender=Network)
pre_save.connect(network_url_id_generator, sender=Network)
pre_save.connect(check_for_plan, sender=Network)
post_save.connect(stat_create_receiver, sender=Network)
pre_save.connect(instance_id_generator, sender=NetworkImage)
pre_save.connect(instance_id_generator, sender=NetworkVideo)
pre_save.connect(instance_id_generator, sender=NetworkDocument)
pre_save.connect(instance_id_generator, sender=NetworkOperationLocation)
pre_save.connect(instance_id_generator, sender=NetworkOperationTiming)
pre_save.connect(instance_id_generator, sender=NetworkReview)
pre_save.connect(instance_id_generator, sender=NetworkJob)
pre_save.connect(instance_id_generator, sender=NetworkStaff)
pre_save.connect(instance_id_generator, sender=NetworkJobOffering)
pre_save.connect(instance_id_generator, sender=NetworkStat)

pre_save.connect(image_label_generator, sender=NetworkImage)
pre_save.connect(video_label_generator, sender=NetworkVideo)
pre_save.connect(document_label_generator, sender=NetworkDocument)