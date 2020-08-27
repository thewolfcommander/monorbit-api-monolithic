from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save

from network.models import Network
from monorbit.utils import tools


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
    payment = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    created = models.DateField(default=timezone.now)
    expiry = models.DateField(default=activity_expiry(365))
    active_till = models.IntegerField(default=365, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)


def instance_id(sender, instance, **kwargs):
    if not instance.id:
        instance.id = tools.random_string_generator(9)

    
def instance_membership_calculator(sender, instance, **kwargs):
    plan = instance.relation.plan
    payment = instance.payment
    if plan.name == "Basic":
        instance.relation.network.is_premium = False
        pass
    else:
        if payment == 0.00:
            instance.active = False
            instance.active_till = 0
            instance.relation.network.is_premium = False
        else:
            instance.active = True
            instance.relation.network.is_premium = True
            no_of_days = float(payment)/float(plan.price_per_day)
            instance.active_till = int(no_of_days)
    instance.expiry = activity_expiry(instance.active_till, instance.created)

    
pre_save.connect(instance_id, sender=NetworkMembershipPlan)
pre_save.connect(instance_id, sender=NetworkMembershipRelation)
pre_save.connect(instance_id, sender=NetworkMembershipActivity)
pre_save.connect(instance_membership_calculator, sender=NetworkMembershipActivity)