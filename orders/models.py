import math
from django.db import models
from django.db.models.signals import pre_save, post_save

from monorbit.utils import tools
from addresses.models import Address
from cart.models import Cart


import logging
logger = logging.getLogger(__name__)


# These choices will be used for processing of orders based on their status 
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
    ('Archived', 'Archived'),
)


# These choices will be used for determining Payment methods for the orders
PAYMENT_METHOD = [
    ('cod', 'Cash on Delivery'),
    ('prepaid', 'Pre paid'),
]


class Order(models.Model):
    """
    This model will handle all the orders placed by users.
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True, help_text="Primary key of the order object")
    day_id = models.IntegerField(default=1, null=True, blank=True, help_text="This would be the day ID of the order. It means if on monday, B Order placed after 12 orders then day_id will be 13 and on tuesday, C Order placed on the morning then its day_id would be 1")
    billing_address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, related_name="billing_address",null=True, blank=True, help_text="Reference to the Address added by the user. This will be used as billing address for the user")
    shipping_address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, related_name="shipping_address", null=True, blank=True, help_text="Reference to the Address added by the user. This will be used as shipping address for the user")
    is_billing_shipping_same = models.BooleanField(default=False, help_text="If true, it means billing address and shipping address are both same. Shipping address can be copied from billing address or can be null.")
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, help_text="Reference to the Cart instance of the user which have been userd to place the order")
    status = models.CharField(max_length=255, default='Created', choices=ORDER_STATUS_CHOICES, null=True, blank=True, help_text="Order Status")
    shipping_total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2, help_text="Shipping total of the order. It means how much user have to pay as shipping charges. Will be copied from cart")
    discount = models.DecimalField(default=0.00, max_digits=100, decimal_places=2, help_text="Discount user got on the order. Will be calculated automatically using discount percentages of each product item.")
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2, help_text="Order total")
    tax = models.DecimalField(default=0.00, max_digits=100, decimal_places=2, help_text="Tax user will be paying for the order")
    payment_method = models.CharField(max_length=255, choices=PAYMENT_METHOD, default='cod', null=True, blank=True, help_text="Payment method opted by the user for the current order")
    active = models.BooleanField(default=True, help_text="If true, it means the order have not been concluded yet. Either it is not delivered or cancelled.")
    is_paid = models.BooleanField(default=False, help_text="If true, it means the payment for the order has been already made")
    is_added_for_received_orders = models.BooleanField(default=False, help_text="If true, it means this order have been used for calculation of recieved order stats for the network")
    is_added_for_sales = models.BooleanField(default=False, help_text="If true, it means this order have been used for sales calculation of network stats")
    is_added_for_total_income = models.BooleanField(default=False, help_text="If true, it means this order have been used for total income calculation of network stats")
    is_added_for_refund = models.BooleanField(default=False, help_text="If true, it means this order have been used for refund calculation of network stats")
    updated = models.DateTimeField(auto_now=True, help_text="Timestamp at which the order has been updated")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="Timestamp at which the order is created")

    def __str__(self):
        """
        This function will be for backend representation of the instance objects for better readability and nothing more like that
        """
        return self.id

    def update_total(self):
        """
        This function will update on trigger using different supporting fields
        """
        cart_total = self.cart.total       # Get the cart total from the cart instance
        shipping_total = 0.00           # Initialize shipping total of order to 0
        new_total = math.fsum([cart_total, shipping_total])         # Calculate the order total by adding cart total and shipping total
        formatted_total = format(new_total, '.2f')          # Format the order total to 2 decimal places
        self.total = formatted_total                   # Assign formatted total to order instance total
        self.shipping_total = shipping_total            # Assign shipping_total to order instance total
        self.save()         # Save the model instance
        return new_total   # return the new order total

def pre_save_create_order_id(sender, instance, *args, **kwargs):
    """
    Trigger function to generate order id
    """
    if not instance.id:
        # Check if id is already generated or not. If not then generate the order id and convert it to uppercase for better readability
        instance.id = tools.random_string_generator().upper()
    # Get the order instance for the current cart. If instance is present, deactivate the order because it is not possible to place two orders using a single cart instance
    qs = Order.objects.filter(cart=instance.cart)
    if qs.exists():
        qs.update(active=False)

    
def post_save_order(sender, instance, created, *args, **kwargs):
    """
    Trigger update total function every time the instance is saved.
    """
    if created:
        print("Updating... first")
        instance.update_total()

    
"""
Connection using signals
"""
pre_save.connect(pre_save_create_order_id, sender=Order)
post_save.connect(post_save_order, sender=Order)