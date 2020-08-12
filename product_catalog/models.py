from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save

from monorbit.utils import tools
from accounts.models import User
from network.models import Network, NetworkCategory


class ProductDefaultCategory(models.Model):
    """
    This would be our product category
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    network_category = models.ForeignKey(NetworkCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    image = models.URLField(null=True, blank=True, default="https://content.monorbit.com/images/placeholder.png")

    def __str__(self):
        return str(self.id)


class ProductDefaultSubCategory(models.Model):
    """
    This would be our product category
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    category = models.ForeignKey(ProductDefaultCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    image = models.URLField(null=True, blank=True, default="https://content.monorbit.com/images/placeholder.png")

    def __str__(self):
        return str(self.id)

    
class ProductCustomCategory(models.Model):
    """
    This would be our product category
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    image = models.URLField(null=True, blank=True, default="https://content.monorbit.com/images/placeholder.png")

    def __str__(self):
        return str(self.id)


class ProductCustomSubCategory(models.Model):
    """
    This would be our product category
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    category = models.ForeignKey(ProductCustomCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    image = models.URLField(null=True, blank=True, default="https://content.monorbit.com/images/placeholder.png")

    def __str__(self):
        return str(self.id)

    
class ProductMeasurement(models.Model):
    """
    MEASUREMENT_CHOICES = [
        ('kg', 'Kilogram'),
        ('gm', 'Gram'),
        ('mg', 'Miligram'),
        ('l', 'Kilogram'),
        ('ml', 'Kilogram'),
        ('piece', 'Dozen'),
        ('dozen', 'Dozen'),
    ]
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    full_form = models.CharField(max_length=112, null=True, blank=True)
    short_form = models.CharField(max_length=25, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)


class Product(models.Model):
    """
    This would be our product category
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    item_code = models.CharField(max_length=112, unique=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    slug = models.CharField(max_length=255, null=True, blank=True)
    brand_name = models.CharField(max_length=255, null=True, blank=True)
    barcode = models.CharField(max_length=255, null=True, blank=True)
    thumbnail_image = models.URLField(null=True, blank=True, default="https://content.monorbit.com/images/placeholder.png")
    mrp = models.DecimalField(default=0.00, max_digits=12, decimal_places=2, help_text="This would be Maximum Retail Price")
    nsp = models.DecimalField(default=0.00, max_digits=12, decimal_places=2, help_text="Net Selling Price - The price at which they offer")
    discount_percent = models.DecimalField(default=0.00, max_digits=12, decimal_places=2, help_text="dp = nsp/mrp * 100")
    tax = models.DecimalField(default=0.00, max_digits=12, decimal_places=2, help_text="Tax on the Product")
    quantity_per_measurement = models.IntegerField(default=1, null=True, blank=True)
    short_description = models.TextField(null=True, blank=True)
    rating = models.DecimalField(default=5.0, max_digits=2, decimal_places=1)
    no_of_reviews = models.IntegerField(null=True, blank=True, default=0)
    available_in_stock = models.IntegerField(null=True, blank=True, default=1)
    
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    default_category = models.ForeignKey(ProductDefaultCategory, on_delete=models.CASCADE, null=True, blank=True)
    custom_category = models.ForeignKey(ProductCustomCategory, on_delete=models.CASCADE, null=True, blank=True)
    default_subcategory = models.ForeignKey(ProductDefaultSubCategory, on_delete=models.CASCADE, null=True, blank=True)
    custom_subcategory = models.ForeignKey(ProductCustomSubCategory, on_delete=models.CASCADE, null=True, blank=True)
    measurement = models.ForeignKey(ProductMeasurement, on_delete=models.CASCADE, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_archived = models.BooleanField(default=False)
    is_open_for_sharing = models.BooleanField(default=False)
    is_digital = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def images(self):
        return self.productimage_set.all()

    @property
    def videos(self):
        return self.productvideo_set.all()

    @property
    def documents(self):
        return self.productdocument_set.all()

    @property
    def tags(self):
        return self.producttag_set.all()

    @property
    def sizes(self):
        return self.productsize_set.all()

    @property
    def specifications(self):
        return self.productspecification_set.all()

    @property
    def extras(self):
        return self.productextra_set.all()


class ProductImage(models.Model):
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    label = models.CharField(max_length=255, null=True, blank=True)
    image = models.URLField(null=True, blank=True)

    def __str__(self):
        return str(self.id)


class ProductVideo(models.Model):
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    label = models.CharField(max_length=255, null=True, blank=True)
    video = models.URLField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

    
class ProductDocument(models.Model):
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    label = models.CharField(max_length=255, null=True, blank=True)
    doc = models.URLField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

    
class ProductTag(models.Model):
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    
class ProductSize(models.Model):
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=255, null=True, blank=True)
    change_side = models.BooleanField(default=True, help_text="If True, then the change would be positive, otherwise - negative")
    price_change = models.DecimalField(default=0.00, max_digits=12, decimal_places=2, help_text="This will be the Price Change from the Original Product Price")

    def __str__(self):
        return str(self.id)

    
class ProductSpecification(models.Model):
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    key = models.CharField(max_length=100, null=True, blank=True)
    value = models.TextField(null=True, blank=True)
    measured_in = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class ProductExtra(models.Model):
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    key = models.CharField(max_length=100, null=True, blank=True)
    value = models.TextField(null=True, blank=True)
    change_side = models.BooleanField(default=True, help_text="If True, then the change would be positive, otherwise - negative")
    price_change = models.DecimalField(default=0.00, max_digits=12, decimal_places=2, help_text="This will be the Price Change from the Original Product Price")

    def __str__(self):
        return str(self.id)


class ProductReview(models.Model):
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    by = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.DecimalField(default=5.0, max_digits=2, decimal_places=1)
    comment = models.TextField(null=True, blank=True)
    is_spam = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)


def instance_id_generator(sender, instance, **kwargs):
    if not instance.id:
        instance.id = tools.random_string_generator(9).upper()

def image_label_generator(sender, instance, **kwargs):
    if not instance.label:
        instance.label = tools.label_gen("IMG-{}".format(str(instance.product.name)))

def video_label_generator(sender, instance, **kwargs):
    if not instance.label:
        instance.label = tools.label_gen("VID-{}".format(str(instance.product.name)))

def document_label_generator(sender, instance, **kwargs):
    if not instance.label:
        instance.label = tools.label_gen("DOC-{}".format(str(instance.product.name)))

    
def product_datainit_generator(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = tools.unique_slug_generator(instance)
    if not instance.item_code:
        instance.item_code = tools.label_gen(instance.network.id)
    instance.discount_percent = float(instance.mrp) - (float(instance.nsp)/float(instance.mrp))*100


pre_save.connect(instance_id_generator, sender=ProductDefaultSubCategory)
pre_save.connect(instance_id_generator, sender=ProductDefaultCategory)
pre_save.connect(instance_id_generator, sender=ProductCustomCategory)
pre_save.connect(instance_id_generator, sender=ProductCustomSubCategory)
pre_save.connect(instance_id_generator, sender=ProductMeasurement)
pre_save.connect(instance_id_generator, sender=Product)
pre_save.connect(instance_id_generator, sender=ProductImage)
pre_save.connect(instance_id_generator, sender=ProductVideo)
pre_save.connect(instance_id_generator, sender=ProductDocument)
pre_save.connect(instance_id_generator, sender=ProductTag)
pre_save.connect(instance_id_generator, sender=ProductSize)
pre_save.connect(instance_id_generator, sender=ProductSpecification)
pre_save.connect(instance_id_generator, sender=ProductExtra)
pre_save.connect(instance_id_generator, sender=ProductReview)

pre_save.connect(product_datainit_generator, sender=Product)
pre_save.connect(image_label_generator, sender=ProductImage)
pre_save.connect(video_label_generator, sender=ProductVideo)
pre_save.connect(document_label_generator, sender=ProductDocument)