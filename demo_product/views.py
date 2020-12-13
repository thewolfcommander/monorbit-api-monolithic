from rest_framework import generics, permissions, pagination

from .serializers import *
from .models import *
from product_catalog.pagination import *



class CreateProductCategory(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductCategoryCreateSerializer
    queryset = ProductCategory.objects.all()


class ListProductCategory(generics.ListAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductCategoryShowSerializer
    queryset = ProductCategory.objects.all()
    filterset_fields = [
        'network_category'
    ]
    pagination_class = CustomPageNumberPagination


class UpdateProductCategory(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductCategoryShowSerializer
    queryset = ProductCategory.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CreateProductSubCategory(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductSubCategoryCreateSerializer
    queryset = ProductSubCategory.objects.all()


class ListProductSubCategory(generics.ListAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductSubCategoryShowSerializer
    queryset = ProductSubCategory.objects.all()
    filterset_fields = [
        'category'
    ]
    pagination_class = CustomPageNumberPagination


class UpdateProductSubCategory(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductSubCategoryShowSerializer
    queryset = ProductSubCategory.objects.all()
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
        'quantity_per_measurement',
        'category',
        'subcategory',
        'measurement',
        'is_active',
        'is_digital',
    ]


class CreateProduct(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductCreateSerializer
    queryset = Product.objects.all()

    # def get_serializer_class(self):
    #     print(self.request)
    #     # if self.request.method:
    #     #     self.serializer_class = ProductShowSerializer
    #     # else:
    #     self.serializer_class = ProductCreateSerializer


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


class UpdateProductImage(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductImageCreateSerializer
    queryset = ProductImage.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UpdateProductVideo(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductVideoCreateSerializer
    queryset = ProductVideo.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UpdateProductDocument(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductDocumentCreateSerializer
    queryset = ProductDocument.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UpdateProductTag(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductTagCreateSerializer
    queryset = ProductTag.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UpdateProductSize(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductSizeCreateSerializer
    queryset = ProductSize.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UpdateProductColor(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductColorCreateSerializer
    queryset = ProductColor.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UpdateProductSpecification(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductSpecificationCreateSerializer
    queryset = ProductSpecification.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UpdateProductExtra(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductExtraCreateSerializer
    queryset = ProductExtra.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
