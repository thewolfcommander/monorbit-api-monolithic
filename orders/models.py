import math
from django.db import models
from django.db.models.signals import pre_save, post_save

from monorbit.utils import tools
from addresses.models import Address
from cart.models import Cart


import logging
logger = logging.getLogger(__name__)

ORDER_STATUS_CHOICES = (
    ('Created', 'Created'),
    ('Confirmed', 'Confirmed'),
    ('Shipped', 'Shipped'),
    ('Dispatched', 'Dispatched'),
    ('Out', 'Out for Delivery'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
    ('Returned', 'Returned'),
    ('Refunded', 'Refunded'),
)


class Order(models.Model):
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    day_id = models.IntegerField(default=1, null=True, blank=True)
    billing_address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, related_name="billing_address")
    shipping_address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, related_name="shipping_address", null=True, blank=True)
    is_billing_shipping_same = models.BooleanField(default=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, default='Created', choices=ORDER_STATUS_CHOICES, null=True, blank=True)
    shipping_total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    discount = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    tax = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = 0.00
        new_total = math.fsum([cart_total, shipping_total])
        formatted_total = format(new_total, '.2f')
        self.total = formatted_total
        self.shipping_total = shipping_total
        self.save()
        return new_total

def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.id:
        instance.id = tools.random_string_generator().upper()
    qs = Order.objects.filter(cart=instance.cart)
    if qs.exists():
        qs.update(active=False)

    
def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        print("Updating... first")
        instance.update_total()

    
pre_save.connect(pre_save_create_order_id, sender=Order)
post_save.connect(post_save_order, sender=Order)