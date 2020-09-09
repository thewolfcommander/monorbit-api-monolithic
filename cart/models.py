from django.db import models
from django.db.models.signals import pre_save
from accounts.models import User
from product_catalog.models import Product

from monorbit.utils import tools


import logging
logger = logging.getLogger(__name__)

    
class Cart(models.Model):
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    count = models.PositiveIntegerField(default=0)
    sub_total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    shipping = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    discount = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    @property
    def products(self):
        return self.productentry_set.all()

    
class ProductEntry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    cost = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.id)

    
def product_cost_calculator(sender, instance, **kwargs):
    instance.cost = float(instance.product.nsp) * int(instance.quantity)


def instance_id(sender, instance, **kwargs):
    if not instance.id:
        instance.id = tools.random_string_generator(9)

    
pre_save.connect(instance_id, sender=Cart)
pre_save.connect(product_cost_calculator, sender=ProductEntry)