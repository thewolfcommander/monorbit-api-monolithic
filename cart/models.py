from django.db import models
from django.db.models.signals import pre_save
from accounts.models import User
from product_catalog.models import *

from monorbit.utils import tools


import logging
logger = logging.getLogger(__name__)


class Wishlist(models.Model):
    """
    Wishlist Model
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    count = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    @property
    def products(self):
        return self.wishlistproductentry_set.all()

    
class WishlistProductEntry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    
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
    PRODUCT_STATUS = [
        ('not_valid', 'Not Valid'),
        ('in_cart', 'In Cart'),
        ('order_created', 'Order Created'),
        ('order_confirmed', 'Order Confirmed'),
        ('order_shipped', 'Order shipped'),
        ('order_dispatched', 'Order dispatched'),
        ('order_out_for_delivery', 'Order out for delivery'),
        ('order_delivered', 'Order Delivered'),
        ('order_cancelled', 'Order Cancelled'),
        ('order_returned', 'Order Returned'),
        ('order_refunded', 'Order Refunded'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    product_status = models.CharField(max_length=255, null=True, blank=True, choices=PRODUCT_STATUS, default="in_cart", help_text="This will determine order status for an individual product")
    quantity = models.IntegerField(default=1, null=True, blank=True)
    size = models.ForeignKey(ProductSize, on_delete=models.CASCADE, null=True, blank=True)
    color = models.ForeignKey(ProductColor, on_delete=models.CASCADE, null=True, blank=True)
    extra = models.ForeignKey(ProductExtra, on_delete=models.CASCADE, null=True, blank=True)
    cost = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.id)

    
def product_cost_calculator(sender, instance, **kwargs):
    instance.cost = (float(instance.product.nsp) * int(instance.quantity)) + float(instance.product.shipping)


def instance_id(sender, instance, **kwargs):
    if not instance.id:
        instance.id = tools.random_string_generator(9)

    
pre_save.connect(instance_id, sender=Cart)
pre_save.connect(instance_id, sender=Wishlist)
pre_save.connect(product_cost_calculator, sender=ProductEntry)