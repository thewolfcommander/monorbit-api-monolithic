from django.db import models

from accounts.models import User
from network.models import Network


class NetworkFollower(models.Model):
    """
    This model is for creating network following
    """
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)