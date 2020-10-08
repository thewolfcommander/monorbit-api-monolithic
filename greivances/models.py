from django.db import models
from django.db.models.signals import pre_save

from accounts.models import User

from monorbit.utils import tools


class FAQCategory(models.Model):
    """
    Model to hold faq categories
    """
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class FAQ(models.Model):
    """
    Model to hold FAQs for Grievances portal
    """
    id = models.CharField(max_length=50, blank=True, unique=True, primary_key=True)
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE)
    question = models.CharField(max_length=512, null=True, blank=True)
    answer = models.TextField(null=True, blank=True)
    popularity_score = models.DecimalField(default=5.00, max_digits=4, decimal_places=2)
    no_of_upvotes = models.IntegerField(default=0, null=True, blank=True)
    no_of_downvotes = models.IntegerField(default=0, null=True, blank=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class FAQReaction(models.Model):
    """
    This model is to keep track on the reactions for FAQs
    """
    faq = models.ForeignKey(FAQ, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    like_it_or_not = models.BooleanField(default=True)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


def instance_id_generator(sender, instance, **args):
    if not instance.id:
        strn = tools.random_string_generator(9)
        instance.id = strn.upper()

pre_save.connect(instance_id_generator, sender=FAQ)