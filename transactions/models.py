from django.db import models

from accounts.models import User
from network.models import Network, NetworkJobOffering
from job_profiles.models import DeliveryBoy, PermanentEmployee, Freelancer


class NetworkFollower(models.Model):
    """
    This model is for creating network following
    """
    network = models.ForeignKey(Network, on_delete=models.CASCADE, help_text="This would be the reference to the Network")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, help_text="This would be reference to the User who is following the network")
    created = models.DateTimeField(auto_now_add=True, help_text="The timestamp at which the user followed the network")

    def __str__(self):
        return str(self.id)

    
class NetworkDeliveryBoyApplication(models.Model):
    """
    This model is for holding network hiring
    """
    # These status helps to identify the application status for which the delivery boy applied to.
    STATUS = [
        ('applied', 'Applied'),
        ('in_touch', 'In Touch'),
        ('hired', 'Hired'),
        ('fired', 'Fired'),
        ('rejected', 'Rejected'),
    ]
    offering = models.ForeignKey(NetworkJobOffering, on_delete=models.CASCADE, help_text="This would be the reference to the Network Job Offering Table. It means this application is going to made to that respective job offering by network.")
    delivery_boy = models.ForeignKey(DeliveryBoy, on_delete=models.CASCADE, help_text="This would be the reference to the delivery boy who is applying to the job offering")
    application_status = models.CharField(max_length=100, null=True, blank=True, choices=STATUS, default='applied', help_text="Job Application status")
    created = models.DateTimeField(auto_now_add=True, help_text="Timestamp at which the delivery boy applied for the job")
    updated = models.DateTimeField(auto_now=True, help_text="Timestamp at which the application has been updated")

    def __str__(self):
        return str(self.id)

    
class NetworkPermanentEmployeeApplication(models.Model):
    """
    This model is for holding network hiring
    """
    STATUS = [
        ('applied', 'Applied'),
        ('in_touch', 'In Touch'),
        ('hired', 'Hired'),
        ('fired', 'Fired'),
        ('rejected', 'Rejected'),
    ]
    offering = models.ForeignKey(NetworkJobOffering, on_delete=models.CASCADE, help_text="This would be the reference to the Network Job Offering Table. It means this application is going to made to that respective job offering by network.")
    permanent_employee = models.ForeignKey(PermanentEmployee, on_delete=models.CASCADE, help_text="This would be the reference to the permanent employee who is applying for the Job Offering")
    application_status = models.CharField(max_length=100, null=True, blank=True, choices=STATUS, default='applied', help_text="Job Application status")
    created = models.DateTimeField(auto_now_add=True, help_text="Timestamp at which the permanent employee applied for the job")
    updated = models.DateTimeField(auto_now=True, help_text="Timestamp at which the application has been updated")

    def __str__(self):
        return str(self.id)

    
class NetworkFreelancerApplication(models.Model):
    """
    This model is for holding network hiring
    """
    STATUS = [
        ('applied', 'Applied'),
        ('in_touch', 'In Touch'),
        ('hired', 'Hired'),
        ('fired', 'Fired'),
        ('rejected', 'Rejected'),
    ]
    offering = models.ForeignKey(NetworkJobOffering, on_delete=models.CASCADE, help_text="This would be the reference to the Network Job Offering Table. It means this application is going to made to that respective job offering by network.")
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE, help_text="This would be the reference to the freelancer who is applying for the Job Offering"))
    application_status = models.CharField(max_length=100, null=True, blank=True, choices=STATUS, default='applied', help_text="Job Application status")
    created = models.DateTimeField(auto_now_add=True, help_text="Timestamp at which the freelancer applied for the job")
    updated = models.DateTimeField(auto_now=True, help_text="Timestamp at which the application has been updated")

    def __str__(self):
        return str(self.id)