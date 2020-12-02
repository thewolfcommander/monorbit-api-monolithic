from django.urls import path
from .views import *

app_name = 'product'

urlpatterns = [
    path('category/default/create/', CreateProductDefaultCategory.as_view(), name='default_category_create'),
    path('category/default/all/', ListProductDefaultCategory.as_view(), name='default_category_all'),
    path('category/default/<slug:id>/', UpdateProductDefaultCategory.as_view(), name='default_category_detail'),

    path('subcategory/default/create/', CreateProductDefaultSubCategory.as_view(), name='default_subcategory_create'),
    path('subcategory/default/all/', ListProductDefaultSubCategory.as_view(), name='default_subcategory_all'),
    path('subcategory/default/<slug:id>/', UpdateProductDefaultSubCategory.as_view(), name='default_subcategory_detail'),

    path('category/custom/', ListCreateProductCustomCategory.as_view(), name='custom_category_all'),
    path('category/custom/<slug:id>/', UpdateProductCustomCategory.as_view(), name='custom_category_update'),

    path('subcategory/custom/all/', ListProductCustomSubCategory.as_view(), name='custom_subcategory_all'),
    path('subcategory/custom/create/', CreateProductCustomSubCategory.as_view(), name='custom_subcategory_create'),
    path('subcategory/custom/<slug:id>/', UpdateProductCustomSubCategory.as_view(), name='custom_subcategory_update'),
    
    path('measurement/', ListCreateProductMeasurement.as_view(), name='measurement_all'),
    path('measurement/<slug:id>/', UpdateProductMeasurement.as_view(), name='measurement_update'),

    path('product/all/', ListProduct.as_view(), name='product_all'),
    path('product/create/', CreateProduct.as_view(), name='product_create'),
    path('product/detail/<slug:slug>/', DetailProduct.as_view(), name='product_detail'),
    path('product/update/<slug:slug>/', UpdateProduct.as_view(), name='product_update'),

    path('product/image/create/', CreateProductImage.as_view(), name='image_create'),
    path('product/video/create/', CreateProductVideo.as_view(), name='video_create'),
    path('product/document/create/', CreateProductDocument.as_view(), name='doc_create'),
    path('product/tag/create/', CreateProductTag.as_view(), name='tag_create'),
    path('product/specification/create/', CreateProductSpecification.as_view(), name='spec_create'),
    path('product/size/create/', CreateProductSize.as_view(), name='size_create'),
    path('product/color/create/', CreateProductColor.as_view(), name='color_create'),
    path('product/extra/create/', CreateProductExtra.as_view(), name='extra_create'),

    path('product/image/update/<slug:id>/', UpdateProductImage.as_view(), name='image_update'),
    path('product/video/update/<slug:id>/', UpdateProductVideo.as_view(), name='video_update'),
    path('product/document/update/<slug:id>/', UpdateProductDocument.as_view(), name='doc_update'),
    path('product/tag/update/<slug:id>/', UpdateProductTag.as_view(), name='tag_update'),
    path('product/specification/update/<slug:id>/', UpdateProductSpecification.as_view(), name='spec_update'),
    path('product/size/update/<slug:id>/', UpdateProductSize.as_view(), name='size_update'),
    path('product/color/update/<slug:id>/', UpdateProductColor.as_view(), name='color_update'),
    path('product/extra/update/<slug:id>/', UpdateProductExtra.as_view(), name='extra_update'),

    path('product/review/create/', CreateProductReview.as_view(), name='review_create'),
    path('product/review/all/', ListProductReview.as_view(), name='review_all'),
    path('product/review/<slug:id>/', UpdateProductReview.as_view(), name='review_update'),
]