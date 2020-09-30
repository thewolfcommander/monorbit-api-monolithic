from django.db import models

from accounts.models import User
from network.models import Network, NetworkJobOffering
from job_profiles.models import DeliveryBoy, PermanentEmployee, Freelancer


class NetworkFollower(models.Model):
    """
    This model is for creating network following
    """
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    
class NetworkDeliveryBoyApplication(models.Model):
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
    offering = models.ForeignKey(NetworkJobOffering, on_delete=models.CASCADE)
    delivery_boy = models.ForeignKey(DeliveryBoy, on_delete=models.CASCADE)
    application_status = models.CharField(max_length=100, null=True, blank=True, choices=STATUS, default='applied')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

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
    offering = models.ForeignKey(NetworkJobOffering, on_delete=models.CASCADE)
    permanent_employee = models.ForeignKey(PermanentEmployee, on_delete=models.CASCADE)
    application_status = models.CharField(max_length=100, null=True, blank=True, choices=STATUS, default='applied')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

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
    offering = models.ForeignKey(NetworkJobOffering, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    application_status = models.CharField(max_length=100, null=True, blank=True, choices=STATUS, default='applied')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)