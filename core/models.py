from django.db import models

# Create your models here.

class TipToGrow(models.Model):
    """
    This model will keep record of all the details about the tps that are going to show on network dashboard.
    """
    tip = models.Textfield(null=True, blank=True)
    upvotes = models.IntegerField(default=0, null=True, blank=True)
    downvotes = models.IntegerField(default=0, null=True, blank=True)
    active = models.BooleanField(default=True)
    adddd = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    
class EmailSentToUsers(models.Model):
    email_type = models.CharField(max_length=255, null=True, blank=True)
    email_sent_to = models.EmailField(null=True, blank=True)
    sent_on = models.