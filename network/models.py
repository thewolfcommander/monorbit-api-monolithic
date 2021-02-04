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
    name = models.CharField(max_length=255, null=True, blank=True, help_text="Name of the network category")
    priority = models.IntegerField(default=2, null=True, blank=True, help_text="Priority of the category. Will be deprecated soon.")
    image = models.URLField(null=True, blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg', help_text="Category Display image")
    created = models.DateTimeField(default=timezone.now, help_text="Timestamp at which the network category is created")


class NetworkType(models.Model):
    """
    This is the network type to which a network belongs to
    """
    name = models.CharField(max_length=255, null=True, blank=True, help_text="Name of the network type")
    image = models.URLField(null=True, blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg', help_text="Network Type display image")
    created = models.DateTimeField(default=timezone.now, help_text="Timestamp at which network type is created")


# class NetworkSubCategory(models.Model):
#     """
#     This is the category for which a network belongs to
#     """
#     name = models.CharField(max_length=255, null=True, blank=True)
#     created = models.DateTimeField(default=timezone.now)


class Network(models.Model):
    """
    This is the base network which a business have to create
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True, help_text="Primary key of the Network")
    urlid = models.CharField(max_length=255, unique=True, blank=True, help_text="This would be the unique username of the network that the netwrk will use for better URL Accessibility")
    network_url = models.URLField(null=True, blank=True, help_text="Public Network URL")
    comment = models.TextField(null=True, blank=True, help_text="This field will tell about the personal comment about the network. Only for admin purpose.")
    user = models.ForeignKey(acc_models.User, on_delete=models.CASCADE, null=True, blank=True, help_text="Reference to the User who is the owner of the network")
    category = models.ForeignKey(NetworkCategory, on_delete=models.CASCADE, null=True, blank=True, help_text="Reference to the Network Category to which this network instance belongs to")
    network_type = models.ForeignKey(NetworkType, on_delete=models.CASCADE, null=True, blank=True, help_text="Reference to the Network Type to which this network instance belongs to")
    name = models.CharField(max_length=255, null=True, blank=True, help_text="Name of the Network")
    thumbnail_image = models.URLField(null=True, blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg', help_text="Logo of the network or the main display image of the network")
    address = models.CharField(max_length=255, null=True, blank=True, help_text="Address of the network")
    landmark = models.CharField(max_length=255, null=True, blank=True, help_text="Landmark near network location")
    city = models.CharField(max_length=255, null=True, blank=True, help_text="City in which network exists primarily")
    state = models.CharField(max_length=255, null=True, blank=True, help_text="State in which network exists primarily")
    country = models.CharField(max_length=255, null=True, blank=True, help_text="Country in which network exists primarily")
    pincode = models.CharField(max_length=10, null=True, blank=True, help_text="PIN code to which network location belongs to")
    alt_phone = models.CharField(validators=[phone_regex,], max_length=17, null=True, blank=True, help_text="This will be the Alternative phone number or the main business phone number")
    alt_email = models.EmailField(
        max_length=255, 
        validators=[EmailValidator], 
        help_text="This will be the alternative email or the main business email",
        null=True,
        blank=True,
    )
    rating = models.DecimalField(default=5.0, max_digits=2, decimal_places=1, help_text="Overall rating of the network given by the users")
    no_of_reviews = models.IntegerField(null=True, blank=True, default=0, help_text="No of reviews given by the users on the network")
    registered_stores = models.IntegerField(null=True, blank=True, default=1, help_text="No of registered stores under a single network")
    followers = models.PositiveIntegerField(null=True, blank=True, default=0, help_text="No of followers of the network, means no of users who have joined the network ")
    
    # Documents Details
    gst = models.CharField(max_length=255, null=True, blank=True, help_text="GST Number of the network")
    adhaar = models.CharField(max_length=255, null=True, blank=True, help_text="Adhaar number of the network owner")
    pan = models.CharField(max_length=255, null=True, blank=True, help_text="PAN Number of the network ownerr")

    # Network Locationa
    lat = models.CharField(max_length=50, null=True, blank=True, help_text="This is the lattitude of the network locations", default="24.67856")
    lng = models.CharField(max_length=50, null=True, blank=True, help_text="This is the longitude of the network locations", default="76.65115")

    # Flags
    is_verified = models.BooleanField(default=False, help_text="This is for verification of uploaded documents")
    is_active = models.BooleanField(default=True, help_text="If true, means network is actively working on Monorbit")
    is_basic = models.BooleanField(default=True, help_text="If true, it means network is using basic plan currently")
    is_economy = models.BooleanField(default=False, help_text="If true, it means network is using economy plan currently")
    is_elite = models.BooleanField(default=False, help_text="If true, it means network is using the elite plan currently")
    is_archived = models.BooleanField(default=False, help_text="If true, it means network is archived or deleted temporarily")
    is_spam = models.BooleanField(default=False, help_text="If true, the network is not valid and is marked as spam or it is fake")
    is_video = models.BooleanField(default=False, help_text="If true, the network have uploaded display video about the network")
    is_document = models.BooleanField(default=False, help_text="If true, the network have uploaded a document about the network like manual, brochure or something like that")

    # Time related fields
    created_on = models.DateTimeField(default=timezone.now, help_text="Timestamp at which the network has been created")
    updated_on = models.DateTimeField(auto_now=True, help_text="Timestamp at which the network has been updated")

    def __str__(self):

        """
        This function will be for backend representation of the instance objects for better readability and nothing more like that
        """
        return str(self.id)

    @property
    def images(self):
        """
        Mapping the array of images object to the network instance
        """
        return self.networkimage_set.all()

    @property
    def videos(self):
        """
        Mapping the array of videos object to the network instance
        """
        return self.networkvideo_set.all()

    @property
    def documents(self):
        """
        Mapping the array of the document object to the network instance
        """
        return self.networkdocument_set.all()

    @property
    def timings(self):
        """
        Mapping the array of network timing object to the network instance
        """
        return self.networkoperationtiming_set.all()

    @property
    def locations(self):
        """
        Mapping the array of network operation locations to the network instance
        """
        return self.networkoperationlocation_set.all()

    @property
    def options(self):
        """
        Mapping all the network options to the network instance
        """
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
    last_updated = models.DateTimeField(auto_now=True, help_text="Timestamp at which the option instance of the network last updated")

    def __str__(self):

        """
        This function will be for backend representation of the instance objects for better readability and nothing more like that
        """
        return str(self.id)


    
class NetworkImage(models.Model):
    """
    This will be the gallery of images that a network will upload to showcase their network on Monorbit
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True, help_text="Primary Key of the Network Image")
    network = models.ForeignKey(Network, on_delete=models.CASCADE, help_text="Reference to the Network who is uploading the image")
    label = models.CharField(max_length=255, null=True, blank=True, help_text="Label for the image specifying what the image depicts actually")
    image = models.URLField(null=True, blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg', help_text="Actual image URL")

    def __str__(self):

        """
        This function will be for backend representation of the instance objects for better readability and nothing more like that
        """
        return str(self.id)


class NetworkVideo(models.Model):
    """
    This will be the videos that a network will upload to showcase their network on Monorbit
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True, help_text="Primary key of the Network Video")
    network = models.ForeignKey(Network, on_delete=models.CASCADE, help_text="Reference to the network who is uploading the video")
    label = models.CharField(max_length=255, null=True, blank=True, help_text="Label for the video specifying what the video depicts actually")
    video = models.URLField(null=True, blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg', help_text="Actual Video URL")

    def __str__(self):

        """
        This function will be for backend representation of the instance objects for better readability and nothing more like that
        """
        return str(self.id)


class NetworkDocument(models.Model):
    """
    This will be the documents that a network will upload to showcase their network on Monorbit
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True, help_text="Primary Key of the Network Document")
    network = models.ForeignKey(Network, on_delete=models.CASCADE, help_text="Reference to the network who is uploading the document")
    label = models.CharField(max_length=255, null=True, blank=True, help_text="Label for the document specifying what the document depicts actually")
    doc = models.URLField(null=True, blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg', help_text="Actual Document URL")

    def __str__(self):

        """
        This function will be for backend representation of the instance objects for better readability and nothing more like that
        """
        return str(self.id)


class NetworkOperationTiming(models.Model):
    """
    This model will keep the record of timing in which network operates
    """
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
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True, help_text="Primary Key of the timing")
    network = models.ForeignKey(Network, on_delete=models.CASCADE, help_text="Reference to the network who is adding the timing")
    day = models.CharField(max_length=255, null=True, blank=True, choices=DAY_CHOICES, default='All', help_text="Day for which timing is being added")
    opening = models.CharField(max_length=25, null=True, blank=True, help_text="Opening time for the day e.g. 10:00 AM")
    status = models.BooleanField(default=True, help_text="If true, means the network is operating for the day. False means network is closed for the day.")
    closing = models.CharField(max_length=25, null=True, blank=True, help_text="Closing time for the day e.g. 06:00 PM")

    def __str__(self):

        """
        This function will be for backend representation of the instance objects for better readability and nothing more like that
        """
        return str(self.id)


class NetworkOperationLocation(models.Model):
    """
    Location in which network provide its delivery or service or operable
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True, help_text="Primary key of the location")
    network = models.ForeignKey(Network, on_delete=models.CASCADE, help_text="Reference to the network who is addding the location")
    pincode = models.CharField(max_length=10, null=True, blank=True, help_text="Pincode in which the network is operational")

    def __str__(self):

        """
        This function will be for backend representation of the instance objects for better readability and nothing more like that
        """
        return str(self.id)


class NetworkReview(models.Model):
    """
    Reviews about the network given by the users
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True, help_text="Primary key of the network reveiew")
    network = models.ForeignKey(Network, on_delete=models.CASCADE, help_text="reference to the network for whom review is going to be added")
    by = models.ForeignKey(acc_models.User, on_delete=models.CASCADE, help_text="Reference to the user who is adding a review about the network")
    rating = models.DecimalField(default=5.0, max_digits=2, decimal_places=1, help_text="Rating that user has given to the network")
    comment = models.TextField(null=True, blank=True, help_text="Comment that the user made on the network")
    is_spam = models.BooleanField(default=False, help_text="If true the review is marked as spam is not valid")
    created = models.DateTimeField(default=timezone.now, help_text="Timestamp at which the review has been created")
    is_active = models.BooleanField(default=True, help_text="If true, the review is active. If false the review has been deactivated")

    def __str__(self):

        """
        This function will be for backend representation of the instance objects for better readability and nothing more like that
        """
        return str(self.id)



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
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True, help_text="Primary Key of the network Job")
    network = models.ForeignKey(Network, on_delete=models.CASCADE, help_text="reference to the network who is creating the Job")
    job_name = models.CharField(max_length=255, null=True, blank=True, help_text="Name of the job e.g. Receptionist")
    job_type = models.CharField(max_length=255, null=True, blank=True, choices=JOB_TYPE, default="permanent", help_text="Type of job")
    job_description = models.TextField(null=True, blank=True, help_text="Description about the job")
    job_requirements = models.TextField(null=True, blank=True, help_text="Requirements for the Job")
    salary_payout_type = models.CharField(max_length=255, null=True, blank=True, choices=SALARY_PAYOUT_TYPE, default="monthly", help_text="It tells how salary is going to be paid in terms of time")
    salary_lower_range = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, help_text="Minimum Salary for the Job")
    salary_upper_range = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, help_text="Maximum salary for the job")
    actual_salary = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, help_text="Actual Salary for the job")
    age_bar_upper = models.IntegerField(default=45, null=True, blank=True, help_text="Maximum age limit for the job")
    age_bar_lower = models.IntegerField(default=18, null=True, blank=True, help_text="Minimum age limit for the job")
    is_active = models.BooleanField(default=True, help_text="If true, the job is currently active")
    is_verified = models.BooleanField(default=False, help_text="If true, job is successfully verified by Monorbit")
    is_spam = models.BooleanField(default=False, help_text="If true, job is marked as spam by Monorbit")
    is_vacant = models.BooleanField(default=True, help_text="If true, job has vacancy")
    created = models.DateTimeField(auto_now_add=True, help_text="Timestamp at which the job has been created by the network")
    updated = models.DateTimeField(auto_now=True, help_text="Timestamp at which the job has been updated")

    def __str__(self):

        """
        This function will be for backend representation of the instance objects for better readability and nothing more like that
        """
        return str(self.id)

    
class NetworkStaff(models.Model):
    """
    This will be the staff of the network
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True, help_text="Primary Key of the Stafff")
    job = models.ForeignKey(NetworkJob, on_delete=models.CASCADE, help_text="Reference to the network job for which this staff has been hired")
    profile = models.ForeignKey(JobProfile, on_delete=models.CASCADE, help_text="Reference to the Job Profile of the Staff who has been selected for the job")
    application_id = models.CharField(max_length=20, null=True, blank=True, help_text="Application ID of the Job Applicant")
    promoted_count = models.IntegerField(default=0, help_text="How much times the staff has been promoted by the network")
    demoted_count = models.IntegerField(default=0, help_text="How much times the staff has been demoted by the network")
    employee_score = models.IntegerField(default=10, help_text="This score would be given to employee out of 10.")
    is_active = models.BooleanField(default=True, help_text="Is the staff is currently working for the network")
    joined = models.DateTimeField(auto_now_add=True, help_text="Timestamp at which the staff joined the network")
    updated = models.DateTimeField(auto_now=True, help_text="Timestamp at which the staff details last updated")

    def __str__(self):

        """
        This function will be for backend representation of the instance objects for better readability and nothing more like that
        """
        return self.id


class NetworkJobOffering(models.Model):
    """
    This model will hold the information about the job offerings for a particular network job. This is the model which will be used for application transactions
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True, help_text="Primary Key of the Job offering")
    job = models.ForeignKey(NetworkJob, on_delete=models.CASCADE, help_text="Reference to the Job for which the offering has been created")
    title = models.CharField(max_length=255, null=True, blank=True, help_text="Title of the Job offering")
    offering_information = models.TextField(null=True, blank=True, help_text="More informatioin about the offering like job details, perks etc.")
    is_active = models.BooleanField(default=True, help_text="If true, it means the offering is active and is accepting applications")
    is_filled = models.BooleanField(default=False, help_text="If true it means the offering has been already filled")
    max_staff_for_job = models.IntegerField(default=5, null=True, blank=True, help_text="Maximum no of staff needed fro the job offering")
    last_date = models.DateField(default=timezone.now, help_text="Last date to apply for the job offering")
    created = models.DateTimeField(auto_now_add=True, help_text="Timestamp at which the offering created")
    updated = models.DateTimeField(auto_now=True, help_text="Timestamp at which the offering has been updated")

    def __str__(self):

        """
        This function will be for backend representation of the instance objects for better readability and nothing more like that
        """
        return str(self.id)


class NetworkStat(models.Model):
    """
    This model will keep the information about the stats of the networks
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True, help_text="Primary Key of the network Stat")
    network = models.ForeignKey(Network, on_delete=models.CASCADE, help_text="Reference to the Network ")
    total_income = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    orders_recieved = models.IntegerField(default=0, null=True, blank=True)
    total_sales = models.IntegerField(default=0, null=True, blank=True, help_text="Total number of meaningful orders")
    refunds = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):

        """
        This function will be for backend representation of the instance objects for better readability and nothing more like that
        """
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

        """
        This function will be for backend representation of the instance objects for better readability and nothing more like that
        """
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