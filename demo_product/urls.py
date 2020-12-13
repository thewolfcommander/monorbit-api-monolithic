from django.urls import path

from .views import *


app_name = 'demo_product'


urlpatterns = [
    # Urls for Categories
    path('category/create/', CreateProductCategory.as_view(), name='create_category'),
    path('category/all/', ListProductCategory.as_view(), name='list_category'),
    path('category/update/<slug:id>/', UpdateProductCategory.as_view(), name='update_category'),

    # Urls for subcategories
    path('subcategory/create/', CreateProductSubCategory.as_view(), name='create_subcategory'),
    path('subcategory/all/', ListProductSubCategory.as_view(), name='list_subcategory'),
    path('subcategory/update/<slug:id>/', UpdateProductSubCategory.as_view(), name='update_subcategory'),

    # Urls for measurement
    path('measurement/', ListCreateProductMeasurement.as_view(), name='list_create_measurement'),
    path('measurement/update/<slug:id>/', UpdateProductMeasurement.as_view(), name='update_measurement'),

    # Product Related urls
    path('products/all/', ListProduct.as_view(), name='list_product'),
    path('products/create/', CreateProduct.as_view(), name='create_product'),
    path('products/detail/<slug:slug>/', DetailProduct.as_view(), name='detail_product'),
    path('products/update/<slug:slug>/', UpdateProduct.as_view(), name='update_product'),

    path('products/image/create/', CreateProductImage.as_view(), name='create_product_image'),
    path('products/image/update/<slug:id>/', UpdateProductImage.as_view(), name='update_product_image'),

    path('products/video/create/', CreateProductVideo.as_view(), name='create_product_video'),
    path('products/video/update/<slug:id>/', UpdateProductVideo.as_view(), name='update_product_video'),

    path('products/document/create/', CreateProductDocument.as_view(), name='create_product_document'),
    path('products/document/update/<slug:id>/', UpdateProductDocument.as_view(), name='update_product_document'),

    path('products/tag/create/', CreateProductTag.as_view(), name='create_product_tag'),
    path('products/tag/update/<slug:id>/', UpdateProductTag.as_view(), name='update_product_tag'),

    path('products/size/create/', CreateProductSize.as_view(), name='create_product_size'),
    path('products/size/update/<slug:id>/', UpdateProductSize.as_view(), name='update_product_size'),

    path('products/color/create/', CreateProductColor.as_view(), name='create_product_color'),
    path('products/color/update/<slug:id>/', UpdateProductColor.as_view(), name='update_product_color'),

    path('products/specification/create/', CreateProductSpecification.as_view(), name='create_product_specification'),
    path('products/specification/update/<slug:id>/', UpdateProductSpecification.as_view(), name='update_product_specification'),
    
    path('products/extra/create/', CreateProductExtra.as_view(), name='create_product_extra'),
    path('products/extra/update/<slug:id>/', UpdateProductExtra.as_view(), name='update_product_extra'),
]