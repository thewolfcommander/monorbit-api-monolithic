from rest_framework import generics, permissions, pagination

from .serializers import *
from .models import *
from .pagination import *


import logging
logger = logging.getLogger(__name__)


class CreateProductDefaultCategory(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductDefaultCategoryCreateSerializer
    queryset = ProductDefaultCategory.objects.all()


class ListProductDefaultCategory(generics.ListAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductDefaultCategoryShowSerializer
    queryset = ProductDefaultCategory.objects.all()
    filterset_fields = [
        'network_category'
    ]
    pagination_class = CustomPageNumberPagination


class UpdateProductDefaultCategory(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductDefaultCategoryShowSerializer
    queryset = ProductDefaultCategory.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CreateProductDefaultSubCategory(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductDefaultSubCategoryCreateSerializer
    queryset = ProductDefaultSubCategory.objects.all()


class ListProductDefaultSubCategory(generics.ListAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductDefaultSubCategoryShowSerializer
    queryset = ProductDefaultSubCategory.objects.all()
    filterset_fields = [
        'category'
    ]
    pagination_class = CustomPageNumberPagination


class UpdateProductDefaultSubCategory(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductDefaultSubCategoryShowSerializer
    queryset = ProductDefaultSubCategory.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ListCreateProductCustomCategory(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductCustomCategorySerializer
    queryset = ProductCustomCategory.objects.all()
    filterset_fields = [
        'network',
    ]


class UpdateProductCustomCategory(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductCustomCategorySerializer
    queryset = ProductCustomCategory.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CreateProductCustomSubCategory(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductCustomSubCategoryCreateSerializer
    queryset = ProductCustomSubCategory.objects.all()


class ListProductCustomSubCategory(generics.ListAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductCustomSubCategoryShowSerializer
    queryset = ProductCustomSubCategory.objects.all()
    filterset_fields = [
        'category'
    ]


class UpdateProductCustomSubCategory(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductCustomSubCategoryShowSerializer
    queryset = ProductCustomSubCategory.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ListCreateProductMeasurement(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductMeasurementSerializer
    queryset = ProductMeasurement.objects.all()
    filterset_fields = [
        'active'
    ]


class UpdateProductMeasurement(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductMeasurementSerializer
    queryset = ProductMeasurement.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    
class ListProduct(generics.ListAPIView):
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
        'default_subcategory',
        'custom_subcategory',
        'measurement',
        'is_active',
        'is_archived',
        'is_open_for_sharing',
        'is_digital',
    ]


class CreateProduct(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductCreateSerializer
    queryset = Product.objects.all()


class DetailProduct(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductShowSerializer
    queryset = Product.objects.all()
    lookup_field = 'slug'


class UpdateProduct(generics.UpdateAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductUpdateSerializer
    queryset = Product.objects.all()
    lookup_field = 'slug'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    
class CreateProductImage(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductImageCreateSerializer
    queryset = ProductImage.objects.all()


class CreateProductVideo(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductVideoCreateSerializer
    queryset = ProductVideo.objects.all()


class CreateProductDocument(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductDocumentCreateSerializer
    queryset = ProductDocument.objects.all()


class CreateProductTag(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductTagCreateSerializer
    queryset = ProductTag.objects.all()


class CreateProductSize(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductSizeCreateSerializer
    queryset = ProductSize.objects.all()


class CreateProductColor(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductColorCreateSerializer
    queryset = ProductColor.objects.all()


class CreateProductSpecification(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductSpecificationCreateSerializer
    queryset = ProductSpecification.objects.all()


class CreateProductExtra(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductExtraCreateSerializer
    queryset = ProductExtra.objects.all()


class CreateProductReview(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductReviewCreateSerializer
    queryset = ProductReview.objects.all()


class ListProductReview(generics.ListAPIView):
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
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductReviewShowSerializer
    queryset = ProductReview.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)