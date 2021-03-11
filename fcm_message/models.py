from django.db import models
from accounts.models import User
from monorbit.utils import tools
from django.db.models.signals import pre_save

class FcmDevice(models.Model):
    DEVICES = [
        ('android','android'),
        ('ios','iso'),
        ('web','wed')
    ]

    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    registration_id = models.CharField(max_length=255,blank=True,null=True)
    device_type = models.CharField(max_length=122,blank=True,null=True,choices=DEVICES,default="web")

    def __str__(self):
        return str(self.registration_id)


    @property
    def messages(self):
        return self.message_set.all()



class Message(models.Model):
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    fcmdevice = models.ForeignKey(FcmDevice,on_delete=models.CASCADE,null=True,blank=True)
    message_title = models.CharField(max_length=512,blank=True,null=True)
    message_body = models.TextField(null=True,blank=True)

    def __str__(self):
        return str(self.message_title)


def instance_id_generator(sender, instance, **kwargs):
    """
    This reciever will generate the primary key of the instances automatically 
    """
    if not instance.id:
        # Checks if the ID of the instance is already present or not. If not then generate the ID using utitlity functions
        instance.id = tools.random_string_generator(9).upper()


pre_save.connect(instance_id_generator, sender=FcmDevice)
pre_save.connect(instance_id_generator,sender=Message)

    