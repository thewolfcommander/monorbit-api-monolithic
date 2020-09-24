from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save

from network.models import Network
from monorbit.utils import tools


import logging
logger = logging.getLogger(__name__)

class NetworkMembershipPlan(models.Model):
    PLAN_CHOICES = [
        ('Basic', 'Basic'),
        ('Economy', 'Economy'),
        ('Elite', 'Elite'),
    ]
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    name = models.CharField(max_length=125, choices=PLAN_CHOICES, default="Basic", null=True, blank=True)
    price_per_day = models.DecimalField(default=0.00, max_digits=6, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    def features(self):
        return self.networkmembershipplanfeatures_set.all()


class NetworkMembershipPlanFeatures(models.Model):
    plan = models.ForeignKey(NetworkMembershipPlan, on_delete=models.CASCADE)
    key = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)

    
class NetworkMembershipRelation(models.Model):
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    network = models.OneToOneField(Network, on_delete=models.CASCADE)
    plan = models.ForeignKey(NetworkMembershipPlan, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


def activity_expiry(days, date=timezone.now()):
    time = date + timezone.timedelta(days=days)
    return time


    
class NetworkMembershipActivity(models.Model):
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    relation = models.ForeignKey(NetworkMembershipRelation, on_delete=models.CASCADE)
    created = models.DateField(default=timezone.now)
    trial_expiry = models.DateField(default=activity_expiry(365))
    trial_active_till = models.IntegerField(default=365, null=True, blank=True)
    trial_applied = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)

    def subscriptions(self):
        return self.networkmembershipsubscription_set.all()


class NetworkMembershipSubscription(models.Model):
    """
    This model will map each individual subscription and payment to activity
    """
    activity = models.ForeignKey(NetworkMembershipActivity, on_delete=models.CASCADE)
    payment_order_id = models.CharField(max_length=100, null=True, blank=True)
    payment = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    started = models.DateField(default=timezone.now)
    is_trial = models.BooleanField(default=False)
    expiry = models.DateField(default=activity_expiry(365))
    active_till = models.IntegerField(default=365, null=True, blank=True)
    active = models.BooleanField(default=True)


class NetworkMembershipInvoice(models.Model):
    """
    THis model will handle invoicing feature
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    subscription = models.ForeignKey(NetworkMembershipSubscription, on_delete=models.CASCADE)
    invoice_period_start_date = models.DateField(null=True, blank=True)
    invoice_period_end_date = models.DateField(null=True, blank=True)
    invoice_description = models.TextField(null=True, blank=True)
    invoice_amount = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    invoice_created = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)


def instance_id(sender, instance, **kwargs):
    if not instance.id:
        instance.id = tools.random_string_generator(9)

def instance_invoice_initializer(sender, instance, **kwargs):
    instance.invoice_period_start_date = instance.subscription.started
    instance.invoice_period_end_date = instance.subscription.expiry
    instance.invoice_description = "Network name - {} has invoiced for subscription {} dated from {} to {} with span of {} days for an amount of INR {}".format(
        instance.subsription.activity.relation.network.name,    
        instance.subscription.id,    
        instance.subsription.started,   
        instance.subsription.expiry,
        instance.subsription.active_till,
        instance.subscription.payment
    )
    instance.invoice_amount = instance.subscription.payment

    
def instance_membership_calculator(sender, instance, **kwargs):
    '''
    The flow should be like:

    First check for plan.
    if plan == basic
        set network premium identity = false
    else
        check for the payment.
        if 
    '''
    plan = instance.activity.relation.plan
    payment = instance.payment
    if plan.name == "Basic":
        instance.activity.relation.network.is_premium = False
        pass
    else:
        if payment == 0.00:
            if instance.activity.trial_applied:
                if timezone.now() >= instance.activity.trial_expiry:
                    instance.activity.active = False
                    instance.active = False
                    instance.active_till = 0
                    instance.activity.relation.network.is_premium = False
                else:
                    pass
            else:
                instance.activity.active = True
                instance.active = True
                instance.is_trial = True
                instance.active_till = 30
                instance.activity.trial_applied = True
                instance.activity.trial_expiry = activity_expiry(30)
                instance.expiry = activity_expiry(30)
                instance.activity.trial_active_till = 30
                instance.activity.relation.network.is_premium = True
        else:
            instance.active = True
            instance.is_trial = False
            instance.activity.active = True
            instance.activity.relation.network.is_premium = True
            no_of_days = float(payment)/float(plan.price_per_day)
            instance.active_till = int(no_of_days)
    instance.expiry = activity_expiry(instance.active_till, instance.started)

    
pre_save.connect(instance_id, sender=NetworkMembershipPlan)
pre_save.connect(instance_id, sender=NetworkMembershipRelation)
pre_save.connect(instance_id, sender=NetworkMembershipActivity)
pre_save.connect(instance_id, sender=NetworkMembershipInvoice)
pre_save.connect(instance_membership_calculator, sender=NetworkMembershipSubscription)