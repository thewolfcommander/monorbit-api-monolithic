from django.db import models
from django.utils import timezone     # This module will be used for time related fields to provide some default values
from django.db.models.signals import pre_save    # This module will be used pre save functionalities of the models

from monorbit.utils import tools    # This module will import useful tools need to be used in signals
from accounts.models import User      # This module will be used only for product review purpose
from network.models import Network, NetworkCategory      # This module will be used in Products and Categories itself.


import logging
logger = logging.getLogger(__name__)


class ProductDefaultCategory(models.Model):
    """
    This would be our product default category - This type of category will be created and provided by ourselves
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True, help_text="Primary Key of the default Product Category")
    network_category = models.ForeignKey(NetworkCategory, on_delete=models.CASCADE, help_text="Reference to the Network category for which this product default category is going to be created or belongs to")
    name = models.CharField(max_length=255, null=True, blank=True, help_text="Name of the Product Default Category")
    image = models.URLField(null=True, blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg', help_text="Display image of the Product Default Category")

    def __str__(self):
        """
        This function will be for backend representation of the instance objects for better readability and nothing more like that
        """
        return str(self.id)


class ProductDefaultSubCategory(models.Model):
    """
    This would be our product default subcategory - This type of subcateory will be created and provided by ourselves 
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True, help_text="Primary Key of the default Product Sub Category")
    category = models.ForeignKey(ProductDefaultCategory, on_delete=models.CASCADE, help_text="Reference to the Product Default Category under which this product default sub category is going to be created or belongs to")
    name = models.CharField(max_length=255, null=True, blank=True, help_text="Name of the Product Default Sub Category")
    image = models.URLField(null=True, blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg', help_text="Display image of the Product Default Sub Category")

    def __str__(self):
        """
        This function will be for backend representation of the instance objects for better readability and nothing more like that
        """
        return str(self.id)

    
class ProductCustomCategory(models.Model):
    """
    This would be our product custom category - This category will be created by the network itself
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True, help_text="Primary Key of the Product Custom Category")
    network = models.ForeignKey(Network, on_delete=models.CASCADE, null=True, blank=True, help_text="Reference to the Network who is creating the particular custom product category or belongs to")
    name = models.CharField(max_length=255, null=True, blank=True, help_text="Name of the Product Custom Category")
    image = models.URLField(null=True, blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg', help_text="Display image of the Product Custom Category")

    def __str__(self):
        """
        This function will be for backend representation of the instance objects for better readability and nothing more like that
        """
        return str(self.id)


class ProductCustomSubCategory(models.Model):
    """
    This would be our product category
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True, help_text="Primary key of the Product Custom Sub Category")
    category = models.ForeignKey(ProductCustomCategory, on_delete=models.CASCADE, help_text="Reference to the Product Custom Category to which this subcategory belongs to or being created for")
    name = models.CharField(max_length=255, null=True, blank=True, help_text="Name of the Product Custom Subcategory")
    image = models.URLField(null=True, blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg', help_text="Display image of the Product Custom Sub Category")

    def __str__(self):
        """
        This function will be for backend representation of the instance objects for better readability and nothing more like that
        """
        return str(self.id)

    
class ProductMeasurement(models.Model):
    """
    This model will keep record of the Measurement Units that we provide for the products
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True, help_text="Primary key of the Product Measurement")
    full_form = models.CharField(max_length=112, null=True, blank=True, help_text="Full form of the Product Measurement Unit, e.g - Kilo Gram")
    short_form = models.CharField(max_length=25, null=True, blank=True, help_text="Short form of the Product Measurement Unit, e.g - KG")
    active = models.BooleanField(default=True, help_text="This field will determine whether the Measurement unit is deprecated or not.")

    def __str__(self):
        """
        This function will be for backend representation of the instance objects for better readability and nothing more like that
        """
        return str(self.id)


class Product(models.Model):
    """
    This would be our original product model - These products are going to be added by the network. They provide necessary information about the product. After that ths product will be used to display on the network page or to place orders on the network.
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True, help_text="Primary Key of the Product")
    item_code = models.CharField(max_length=112, unique=True, blank=True, help_text="Unique Item Code for the Product. This will be used for advanced purposes in the future.")
    name = models.CharField(max_length=255, null=True, blank=True, help_text="Product Name")
    slug = models.CharField(max_length=255, null=True, blank=True, unique=True, help_text="Product Slug automatcially generated from the product's name")
    brand_name = models.CharField(max_length=255, null=True, blank=True, help_text="Products brand name - Eg. Gucci")
    barcode = models.CharField(max_length=255, null=True, blank=True, help_text="Products bar code")
    thumbnail_image = models.URLField(null=True, blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg', help_text="Products thumbnail image - This will be short image that can be used for specific purposes")
    mrp = models.DecimalField(default=0.00, max_digits=12, decimal_places=2, help_text="This would be Maximum Retail Price")
    nsp = models.DecimalField(default=0.00, max_digits=12, decimal_places=2, help_text="Net Selling Price - The price at which they offer")
    discount_percent = models.DecimalField(default=0.00, max_digits=12, decimal_places=2, help_text="dp = nsp/mrp * 100")
    tax = models.DecimalField(default=0.00, max_digits=12, decimal_places=2, help_text="Tax on the Product")
    shipping = models.DecimalField(default=0.00, max_digits=12, decimal_places=2, help_text="Shipping charge for the product")
    quantity_per_measurement = models.IntegerField(default=1, null=True, blank=True, help_text="This would be quantity for measurement unit - e.g. 100gm, 100 is quantity and gm is unit")
    short_description = models.TextField(null=True, blank=True, help_text="Short Description about the product")
    rating = models.DecimalField(default=5.0, max_digits=2, decimal_places=1, help_text="Rating for the product that users have given")
    no_of_reviews = models.IntegerField(null=True, blank=True, default=0, help_text="No of total reviews that have given on the product by users")
    available_in_stock = models.IntegerField(null=True, blank=True, default=1, help_text="No of quantity of product which is available in stock")
    minimum_quantity_per_order = models.IntegerField(null=True, blank=True, default=1, help_text="Minimum no of quantity that need to be placed for the order of this particular product")
    
    network = models.ForeignKey(Network, on_delete=models.CASCADE, help_text="Reference to the Network who have added the Product")
    default_category = models.ForeignKey(ProductDefaultCategory, on_delete=models.CASCADE, null=True, blank=True, help_text="Reference to the Default Product Category for which the product have been added. Can be replaceable with Custom Product Category")
    custom_category = models.ForeignKey(ProductCustomCategory, on_delete=models.CASCADE, null=True, blank=True, help_text="Reference to the Custom Product Category for which the product have been added. Can be relplaceable with Default Product Category. Should only be one of these present, not both of them for any product")
    default_subcategory = models.ForeignKey(ProductDefaultSubCategory, on_delete=models.CASCADE, null=True, blank=True, help_text="Reference to the Default Sub Category for which the product have been added. Should only be paired with Default Product Category")
    custom_subcategory = models.ForeignKey(ProductCustomSubCategory, on_delete=models.CASCADE, null=True, blank=True, help_text="Reference to the Custom Product Sub Category for which the product have been added. Should only be paired with Custom Product Category")
    measurement = models.ForeignKey(ProductMeasurement, on_delete=models.CASCADE, null=True, blank=True, help_text="Reference to the Measurement in which the product is going to be measured")

    created = models.DateTimeField(auto_now_add=True, help_text="Timestamp at which the product have been added")
    updated = models.DateTimeField(auto_now=True, help_text="Timestamp at which the product have been updated")

    is_refundable = models.BooleanField(default=False, null=True, blank=True, help_text="Is the current product is refundable?")
    is_stock_unlimited = models.BooleanField(default=False, null=True, blank=True, help_text="Is the stock is unlimited for the product")
    is_returnable = models.BooleanField(default=False, null=True, blank=True, help_text="Is the current product is returnable?")
    is_active = models.BooleanField(default=True, help_text="Is the current product is active or being deactivated?")
    is_archived = models.BooleanField(default=False, help_text="Is the current product have been moved to the archived vault?")
    is_open_for_sharing = models.BooleanField(default=False, help_text="Is the network is ready to share the product data with the other sellers")
    is_digital = models.BooleanField(default=False, help_text="Is the product is going to be sold digitally and has no physical significance. like a software or a movie being transfered through FTP.")

    def __str__(self):
        """
        This function will be for backend representation of the instance objects for better readability and nothing more like that
        """
        return str(self.id)

    @property
    def images(self):
        """
        Mapping the array of product images to product instance
        """
        return self.productimage_set.all()

    @property
    def videos(self):
        """
        Mapping the array of product videos to product instance
        """
        return self.productvideo_set.all()

    @property
    def documents(self):
        """
        Mapping the array of product documents to product instance
        """
        return self.productdocument_set.all()

    @property
    def tags(self):
        """
        Mapping the array of product tags to product instance
        """
        return self.producttag_set.all()

    @property
    def sizes(self):
        """
        Mapping the array of available sizes for the product to product instance
        """
        return self.productsize_set.all()

    @property
    def colors(self):
        """
        Mapping the array of the available color options for the product to product instance
        """
        return self.productcolor_set.all()

    @property
    def specifications(self):
        """
        Mapping the array of product specification objects for the product to product instance
        """
        return self.productspecification_set.all()

    @property
    def extras(self):
        """
        Mapping the extra available options for the product to product instance
        """
        return self.productextra_set.all()


class ProductImage(models.Model):
    """
    This model will keep all the gallery images for the product.
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True, help_text="Primary Key of the Product Image")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, help_text="Reference to the product for which this image belongs to")
    label = models.CharField(max_length=255, null=True, blank=True, help_text="Label of the image. It means what the image depits actually")
    image = models.URLField(null=True, blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg', help_text="Actual URL of the image. This URL will be filled automatically after uploading the image to the Storage Bucket")

    def __str__(self):
        """
        This function will be for backend representation of the instance objects for better readability and nothing more like that
        """
        return str(self.id)


class ProductVideo(models.Model):
    """
    This model will keep all the gallery videos for the product
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True, help_text="Primary key of the Product Video")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, help_text="Reference to the product for which this video belongs to")
    label = models.CharField(max_length=255, null=True, blank=True, help_text="Label of the video. It means wht the image depicts actually")
    video = models.URLField(null=True, blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg', help_text="Actual URL of the video. This URL will be filled automatically after uploading the video to the Storage Bucket")

    def __str__(self):
        """
        This function will be for backend representation of the instance objects for better readability and nothing more like that
        """
        return str(self.id)

    
class ProductDocument(models.Model):
    """
    This model will keep all the Documents for the product
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True, help_text="Primary Key of the Product Document")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, help_text="Reference to the product for which this document belongs to")  
    label = models.CharField(max_length=255, null=True, blank=True, help_text="Lable of the document. It means what the document depicts actually")
    doc = models.URLField(null=True, blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg', help_text="Actual URL of the document")

    def __str__(self):
        """
        This function will be for backend representation of the instance objects for better readability and nothing more like that
        """
        return str(self.id)

    
class ProductTag(models.Model):
    """
    This model will keep all the tags added for the product
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True, help_text="Primary Key of the Product Tag")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, help_text="Reference to the Product for which this tag belongs to")
    name = models.CharField(max_length=255, null=True, blank=True, help_text="Name of the tag e.g Best Earphone below 200")

    def __str__(self):
        """
        This function will be for backend representation of the instance objects for better readability and nothing more like that
        """
        return str(self.id)

    
class ProductSize(models.Model):
    """
    This model will keep all the sizes added for the product. These will be the size options available for a particular product
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True, help_text="Primary Key of the Product Size")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, help_text="Reference to the Product to which this size belongs to")
    size = models.CharField(max_length=255, null=True, blank=True, help_text="Size title e.g. 4GB+32GB")
    change_side = models.BooleanField(default=True, help_text="If True, then the change would be positive, otherwise - negative")
    price_change = models.DecimalField(default=0.00, max_digits=12, decimal_places=2, help_text="This will be the Price Change from the Original Product Price")

    def __str__(self):
        """
        This function will be for backend representation of the instance objects for better readability and nothing more like that
        """
        return str(self.id)


class ProductColor(models.Model):
    """
    This model will keep all the color options for the product
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True, help_text="Primary key of the Product Color")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, help_text="Reference to the Product to which this color belongs to")
    color = models.CharField(max_length=255, null=True, blank=True, help_text="Title of the color e.g. Royal Black")
    change_side = models.BooleanField(default=True, help_text="If True, then the change would be positive, otherwise - negative")
    price_change = models.DecimalField(default=0.00, max_digits=12, decimal_places=2, help_text="This will be the Price Change from the Original Product Price")

    def __str__(self):
        """
        This function will be for backend representation of the instance objects for better readability and nothing more like that
        """
        return str(self.id)

    
class ProductSpecification(models.Model):
    """
    Product Specifications are the extra bit of information or features that network want to display to the user in a really organized manner.

    Exmple:

    Suppose a Phone have RAM of 4GB and ROM of 64GB then here these specifications can be mentioned in a more organized manner
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True, help_text="Primary Key of the Product Specification")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, help_text="Reference to the Product to which this specification belongs to")
    key = models.CharField(max_length=100, null=True, blank=True, help_text="Key of the Specification e.g. RAM here is the Key")
    value = models.TextField(null=True, blank=True, help_text="Value of the Specification e.g. 4 is the Value here")
    measured_in = models.CharField(max_length=50, null=True, blank=True, help_text="Measuring unit of the Specification e.g. GB is the measurement unit here")

    def __str__(self):
        """
        This function will be for backend representation of the instance objects for better readability and nothing more like that
        """
        return str(self.id)


class ProductExtra(models.Model):
    """
    Product Extras are the Extra Product add ons that network can add for more user convenience
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True, help_text="Primary Key of the Product Extra")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, help_text="Reference to the Product to which this extra add on belongs to")
    key = models.CharField(max_length=100, null=True, blank=True, help_text="Key of the Extra add on e.g. Earphone")
    value = models.TextField(null=True, blank=True, help_text="Value of the Extra add on e.g. Wireless bluetooth earphone with 30h battery life is the Value here")
    change_side = models.BooleanField(default=True, help_text="If True, then the change would be positive, otherwise - negative")
    price_change = models.DecimalField(default=0.00, max_digits=12, decimal_places=2, help_text="This will be the Price Change from the Original Product Price")

    def __str__(self):
        """
        This function will be for backend representation of the instance objects for better readability and nothing more like that
        """
        return str(self.id)


class ProductReview(models.Model):
    id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True, help_text="Primary Key of the Product Review")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, help_text="Reference to the Product for which the review have given") 
    by = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Reference to the user who have given the review")
    rating = models.DecimalField(default=5.0, max_digits=2, decimal_places=1, help_text="This will tell how much the user rated the product - It varies between 1 and 5")
    comment = models.TextField(null=True, blank=True, help_text="Tells about the comment user leaved about the product in the review")
    is_spam = models.BooleanField(default=False, help_text="If true, the review will be marked as spam and will not be considered for product rating calculation")
    created = models.DateTimeField(default=timezone.now, help_text="Timestamp at which the user have given the review on the product")
    is_active = models.BooleanField(default=True, help_text="If true, the review is active. If false, review is no more valid.")

    def __str__(self):
        """
        This function will be for backend representation of the instance objects for better readability and nothing more like that
        """
        return str(self.id)

class ProductTopping(models.Model):
    id = models.CharField(max_length=10,primary_key=True,unique=True,blank=True,help_text="Primary key of the Product topping")
    topping = models.CharField(max_length=255,blank=True,null=True,help_text="Topping name")
    description = models.TextField(blank=True,null=True,help_text="Description of the product's topping.")
    price_change = models.DecimalField(max_digits=3,decimal_places=2,help_text="Price of toppins")
    up_down_side = models.BooleanField(default=False)

    def __str__(self):
        return str(self.topping)


"""

RECIEVERS FOR SPECIAL TASKS RELATED TO INSTANCES

"""

def instance_id_generator(sender, instance, **kwargs):
    """
    This reciever will generate the primary key of the instances automatically 
    """
    if not instance.id:
        # Checks if the ID of the instance is already present or not. If not then generate the ID using utitlity functions
        instance.id = tools.random_string_generator(9).upper()


def image_label_generator(sender, instance, **kwargs):
    """
    This will generate a label for the image if not provided, by using the product name
    """
    if not instance.label:
        instance.label = tools.label_gen("IMG-{}".format(str(instance.product.name)))


def video_label_generator(sender, instance, **kwargs):
    """
    This will generate a label for the video if not provided, by using the product name
    """
    if not instance.label:
        instance.label = tools.label_gen("VID-{}".format(str(instance.product.name)))


def document_label_generator(sender, instance, **kwargs):
    """
    This will generate a label for the document if not provided, by using the product name
    """
    if not instance.label:
        instance.label = tools.label_gen("DOC-{}".format(str(instance.product.name)))

    
def product_datainit_generator(sender, instance, **kwargs):
    """
    This function initiates some proesses that needs to be done before saving a product
    """
    # Check for any change in the instance and generate the slug everytime using the product name
    instance.slug = tools.unique_slug_generator(instance)
    if not instance.item_code:
        # Check if item_code of the product has been generated or not. If not, generate the item code using utility functions
        instance.item_code = tools.label_gen(instance.network.id)

    # Calculate the dicsount percestage everytime the product instance is saved
    instance.discount_percent = ((float(instance.mrp)-float(instance.nsp))/float(instance.mrp))*100


"""
CONNECTORS 
"""

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
pre_save.connect(instance_id_generator, sender=ProductColor)
pre_save.connect(instance_id_generator, sender=ProductSpecification)
pre_save.connect(instance_id_generator, sender=ProductExtra)
pre_save.connect(instance_id_generator, sender=ProductReview)
pre_save.connect(instance_id_generator, sender=ProductTopping)


pre_save.connect(product_datainit_generator, sender=Product)
pre_save.connect(image_label_generator, sender=ProductImage)
pre_save.connect(video_label_generator, sender=ProductVideo)
pre_save.connect(document_label_generator, sender=ProductDocument)