from rest_framework import generics, permissions, pagination

from .serializers import *
from .models import *
from .pagination import *
from .permissions import *


import logging
logger = logging.getLogger(__name__)


class CreateProductDefaultCategory(generics.CreateAPIView):
    """
    Default category of product which is provided by monorbit. Only Admin can create product category.
    """
    permission_classes = [ProductAdminPermission]
    serializer_class = ProductDefaultCategoryCreateSerializer
    queryset = ProductDefaultCategory.objects.all()


class ListProductDefaultCategory(generics.ListAPIView):
    """
    Product default category list, will provided to network creator.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductDefaultCategoryShowSerializer
    queryset = ProductDefaultCategory.objects.all()
    filterset_fields = [
        'network_category'
    ]
    pagination_class = CustomPageNumberPagination


class UpdateProductDefaultCategory(generics.RetrieveUpdateDestroyAPIView):
    """
    Updating (put, patch, delete) product default category. Only admin can do it.
    """
    permission_classes = [ProductDetailAdminPermission]
    serializer_class = ProductDefaultCategoryShowSerializer
    queryset = ProductDefaultCategory.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CreateProductDefaultSubCategory(generics.CreateAPIView):
    """
    Default subcategory of product which is provided by monorbit. Only Admin can create product subcategory.
    """
    permission_classes = [ProductAdminPermission]
    serializer_class = ProductDefaultSubCategoryCreateSerializer
    queryset = ProductDefaultSubCategory.objects.all()


class ListProductDefaultSubCategory(generics.ListAPIView):
    """
    Product default subcategory list, will provided to network creator.
    """
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductDefaultSubCategoryShowSerializer
    queryset = ProductDefaultSubCategory.objects.all()
    filterset_fields = [
        'category'
    ]
    pagination_class = CustomPageNumberPagination


class UpdateProductDefaultSubCategory(generics.RetrieveUpdateDestroyAPIView):
    """
    Updating (put, patch, delete) product default subcategory. Only admin can do it.
    """
    permission_classes = [ProductDetailAdminPermission]
    serializer_class = ProductDefaultSubCategoryShowSerializer
    queryset = ProductDefaultSubCategory.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ListCreateProductCustomCategory(generics.ListCreateAPIView):
    """
    Network creator can introduce new product category.
    List of all product custom categories.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    serializer_class = ProductCustomCategorySerializer
    queryset = ProductCustomCategory.objects.all()
    filterset_fields = [
        'network',
    ]


class UpdateProductCustomCategory(generics.RetrieveUpdateDestroyAPIView):
    """
    Network creator can update(put, patch, delete) their product custom categories.
    """
    permission_classes = [IsSubPartOwner]
    serializer_class = ProductCustomCategorySerializer
    queryset = ProductCustomCategory.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CreateProductCustomSubCategory(generics.CreateAPIView):
    """
    Network creator can introduce new product subcategory.
    """
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = ProductCustomSubCategoryCreateSerializer
    queryset = ProductCustomSubCategory.objects.all()


class ListProductCustomSubCategory(generics.ListAPIView):
    """
    List of all product custom subcategories.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    serializer_class = ProductCustomSubCategoryShowSerializer
    queryset = ProductCustomSubCategory.objects.all()
    filterset_fields = [
        'category'
    ]


class UpdateProductCustomSubCategory(generics.RetrieveUpdateDestroyAPIView):
    """
    Network creator can update(put, patch, delete) their product custom subcategories.
    """
    permission_classes = [IsSubSubPartOwner,]
    serializer_class = ProductCustomSubCategoryShowSerializer
    queryset = ProductCustomSubCategory.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ListCreateProductMeasurement(generics.ListCreateAPIView):
    """
    Product measurements ('kg', 'Kilogram'),
        ('gm', 'Gram'),
        ('mg', 'Miligram'),
        ('l', 'Kilogram'),
    Only admin can create.
    List of all Product Measurements, will provided to network creator.
    """
    permission_classes = [ProductAdminPermission,]
    serializer_class = ProductMeasurementSerializer
    queryset = ProductMeasurement.objects.all()
    filterset_fields = [
        'active'
    ]


class UpdateProductMeasurement(generics.RetrieveUpdateDestroyAPIView):
    """
    Only admin can update product measurements.
    """
    permission_classes = [ProductDetailAdminPermission,]
    serializer_class = ProductMeasurementSerializer
    queryset = ProductMeasurement.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    
class ListProduct(generics.ListAPIView):
    """
    List of products.
    """
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductShowSerializer
    queryset = Product.objects.all()
    filterset_fields = [
        'brand_name',
        'barcode',
        'mrp',
        'nsp',
        'discount_percent',
        'tax',
        'quantity_per_measurement',
        'rating',
        'no_of_reviews',
        'available_in_stock',
        'network',
        'default_category',
        'custom_category',
        'is_stock_unlimited',
        'default_subcategory',
        'custom_subcategory',
        'measurement',
        'is_active',
        'is_archived',
        'is_open_for_sharing',
        'is_digital',
    ]


class CreateProduct(generics.CreateAPIView):
    """
    Network creator can add their products in network.
    """
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = ProductCreateSerializer
    queryset = Product.objects.all()

    # def get_serializer_class(self):
    #     print(self.request)
    #     # if self.request.method:
    #     #     self.serializer_class = ProductShowSerializer
    #     # else:
    #     self.serializer_class = ProductCreateSerializer


class DetailProduct(generics.RetrieveDestroyAPIView):
    """
    Network creator can delete their products.
    """
    permission_classes = [IsSubPartDetailOwner,]
    serializer_class = ProductShowSerializer
    queryset = Product.objects.all()
    lookup_field = 'slug'


class UpdateProduct(generics.UpdateAPIView):
    """
    Network creator can update(put and patch) their products.
    """
    permission_classes = [IsSubPartDetailOwner,]
    serializer_class = ProductUpdateSerializer
    queryset = Product.objects.all()
    lookup_field = 'slug'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    
class CreateProductImage(generics.CreateAPIView):
    """
    Product Image will be uploaded here.(Only network creator and product owner)
    """
    permission_classes = [IsProductOwnersVariant]
    serializer_class = ProductImageCreateSerializer
    queryset = ProductImage.objects.all()

    # def perform_create(self,serializer):
    #     print(serializer["product"])



class CreateProductVideo(generics.CreateAPIView):
    """
    Product video will be uploaded here.(Only network creator and product owner)
    """
    permission_classes = [IsProductOwnersVariant]
    serializer_class = ProductVideoCreateSerializer
    queryset = ProductVideo.objects.all()


class CreateProductDocument(generics.CreateAPIView):
    """
    Product document(pamplets,poster) will be uploaded here.(Only network creator and product owner)
    """
    permission_classes = [IsProductOwnersVariant]
    serializer_class = ProductDocumentCreateSerializer
    queryset = ProductDocument.objects.all()


class CreateProductTag(generics.CreateAPIView):
    """
    Tags related to product.(Only network creator and product owner)
    """
    permission_classes = [IsProductOwnersVariant]
    serializer_class = ProductTagCreateSerializer
    queryset = ProductTag.objects.all()


class CreateProductSize(generics.CreateAPIView):
    """
    Product size will be uploaded here.(Only network creator and product owner)
    """
    permission_classes = [IsProductOwnersVariant]
    serializer_class = ProductSizeCreateSerializer
    queryset = ProductSize.objects.all()


class CreateProductColor(generics.CreateAPIView):
    """
    Product color will be uploaded here.(Only network creator and product owner)
    """
    permission_classes = [IsProductOwnersVariant]
    serializer_class = ProductColorCreateSerializer
    queryset = ProductColor.objects.all()


class CreateProductSpecification(generics.CreateAPIView):
    """
    Product specification will be uploaded here.(Only network creator and product owner)
    """
    permission_classes = [IsProductOwnersVariant]
    serializer_class = ProductSpecificationCreateSerializer
    queryset = ProductSpecification.objects.all()


class CreateProductExtra(generics.CreateAPIView):
    """
    Product extra property will be uploaded here.(Only network creator and product owner)
    """
    permission_classes = [IsProductOwnersVariant]
    serializer_class = ProductExtraCreateSerializer
    queryset = ProductExtra.objects.all()

class CreateProductTopping(generics.CreateAPIView):
    """
    Toppings for product. 
    """
    permission_classes = []
    serializer_class = ProductToppingCreateSerializer
    queryset = ProductTopping.objects.all()


class UpdateProductImage(generics.RetrieveUpdateDestroyAPIView):
    """
    Product image will be updated(put,patch,delete) here.(Only network creator and product owner)
    """
    permission_classes = [IsProductOwnersVariantDetail]
    serializer_class = ProductImageCreateSerializer
    queryset = ProductImage.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UpdateProductVideo(generics.RetrieveUpdateDestroyAPIView):
    """
    Product video will be updated(put,patch,delete) here.(Only network creator and product owner)
    """
    permission_classes = [IsProductOwnersVariantDetail]
    serializer_class = ProductVideoCreateSerializer
    queryset = ProductVideo.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UpdateProductDocument(generics.RetrieveUpdateDestroyAPIView):
    """
    Product document will be updated(put,patch,delete) here.(Only network creator and product owner)
    """
    permission_classes = [IsProductOwnersVariantDetail]
    serializer_class = ProductDocumentCreateSerializer
    queryset = ProductDocument.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UpdateProductTag(generics.RetrieveUpdateDestroyAPIView):
    """
    Tags related to product will be updated(put,patch,delete) here.(Only network creator and product owner)
    """
    permission_classes = [IsProductOwnersVariantDetail]
    serializer_class = ProductTagCreateSerializer
    queryset = ProductTag.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UpdateProductSize(generics.RetrieveUpdateDestroyAPIView):
    """
    Product size will be updated(put,patch,delete) here.(Only network creator and product owner)
    """
    permission_classes = [IsProductOwnersVariantDetail]
    serializer_class = ProductSizeCreateSerializer
    queryset = ProductSize.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UpdateProductColor(generics.RetrieveUpdateDestroyAPIView):
    """
    Product color will be updated(put,patch,delete) here.(Only network creator and product owner)
    """
    permission_classes = [IsProductOwnersVariantDetail]
    serializer_class = ProductColorCreateSerializer
    queryset = ProductColor.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UpdateProductSpecification(generics.RetrieveUpdateDestroyAPIView):
    """
    Product specification will be updated(put,patch,delete) here.(Only network creator and product owner)
    """
    permission_classes = [IsProductOwnersVariantDetail]
    serializer_class = ProductSpecificationCreateSerializer
    queryset = ProductSpecification.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UpdateProductExtra(generics.RetrieveUpdateDestroyAPIView):
    """
    Product extra proverties will be updated(put,patch,delete) here.(Only network creator and product owner)
    """
    permission_classes = [IsProductOwnersVariantDetail]
    serializer_class = ProductExtraCreateSerializer
    queryset = ProductExtra.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class UpdateProductTopping(generics.RetrieveUpdateDestroyAPIView):
    """
    Toppings will update here.
    """
    permission_classes = []
    serializer_class = ProductToppingCreateSerializer
    queryset = ProductTopping.objects.all()
    lookup_field = 'id'

    def patch(self,request,*args,**kwargs):
        return self.partial_update(request,*args,**kwargs)


class CreateProductReview(generics.CreateAPIView):
    """
    Normal user will give review(comment) and rating to any product according to his experience.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductReviewCreateSerializer
    queryset = ProductReview.objects.all()


class ListProductReview(generics.ListAPIView):
    """
    List of all reviews, given to a product.
    """
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductReviewShowSerializer
    queryset = ProductReview.objects.all()
    filterset_fields = [
        'product',
        'by',
        'rating',
        'is_spam',
        'is_active'
    ]


class UpdateProductReview(generics.UpdateAPIView):
    """
    Normal user who give review, can update their review.
    """
    permission_classes = [IsReviewOwner]
    serializer_class = ProductReviewShowSerializer
    queryset = ProductReview.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)