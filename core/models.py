from django.db import models

# Create your models here.

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