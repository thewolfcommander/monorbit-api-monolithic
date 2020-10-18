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
    image_url = models.URLField(null=True, blank=True, default='https://www.freeiconspng.com/thumbs/platform-icon/platform-icon-12.png')
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

    
class TicketCategory(models.Model):
    """
    This would be category of the issue ticket
    """
    title = models.CharField(max_length=255, null=True, blank=True)
    icon = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

    
class Ticket(models.Model):
    """
    This would be the ticket information
    """
    TICKET_STATUS = [
        ('created', 'Created'),
        ('in_process', 'In Process'),
        ('resolved', 'Resolved'),
        ('spam', 'Spam'),
        ('half_resolved', 'Half Resolved'),
    ]
    id = models.CharField(max_length=20, blank=True, primary_key=True, unique=True)
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    monion_referral = models.CharField(max_length=255, null=True, blank=True)
    country_code = models.IntegerField(default=91, null=True, blank=True)
    mobile_number = models.CharField(max_length=10, null=True, blank=True)
    define_category = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    ticket_status = models.CharField(max_length=255, null=True, blank=True, default='created', choices=TICKET_STATUS)
    upvotes = models.IntegerField(default=0, null=True, blank=True)
    downvotes = models.IntegerField(default=0, null=True, blank=True)
    is_attachment = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    def attachments(self):
        return self.ticketattachment_set.all()

    def comments(self):
        return self.ticketcomment_set.all()

    
class TicketAttachment(models.Model):
    """
    Attachments linked to ticket
    """
    TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('doc', 'Document'),
        ('audio', 'Audio')
    ]
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    attachment_type = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return str(self.id)


class TicketComment(models.Model):
    """
    Comments or resolutions made on ticket
    """
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    upvotes = models.IntegerField(default=0, null=True, blank=True)
    downvotes = models.IntegerField(default=0, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


def instance_id_generator(sender, instance, **args):
    if not instance.id:
        strn = tools.random_string_generator(9)
        instance.id = strn.upper()

pre_save.connect(instance_id_generator, sender=FAQ)
pre_save.connect(instance_id_generator, sender=Ticket)