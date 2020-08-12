from django.urls import path
from .views import *


urlpatterns = [
    path('category/default/create/', CreateProductDefaultCategory.as_view()),
    path('category/default/all/', ListProductDefaultCategory.as_view()),
    path('category/default/<slug:id>/', UpdateProductDefaultCategory.as_view()),

    path('subcategory/default/create/', CreateProductDefaultSubCategory.as_view()),
    path('subcategory/default/all/', ListProductDefaultSubCategory.as_view()),
    path('subcategory/default/<slug:id>/', UpdateProductDefaultSubCategory.as_view()),

    path('category/custom/', ListCreateProductCustomCategory.as_view()),
    path('category/custom/<slug:id>/', UpdateProductCustomCategory.as_view()),

    path('subcategory/custom/all/', ListProductCustomSubCategory.as_view()),
    path('subcategory/custom/create/', CreateProductCustomSubCategory.as_view()),
    path('subcategory/custom/<slug:id>/', UpdateProductCustomSubCategory.as_view()),
    
    path('measurement/', ListCreateProductMeasurement.as_view()),
    path('measurement/<slug:id>/', UpdateProductMeasurement.as_view()),

    path('product/all/', ListProduct.as_view()),
    path('product/create/', CreateProduct.as_view()),
    path('product/detail/<slug:slug>/', DetailProduct.as_view()),
    path('product/update/<slug:slug>/', UpdateProduct.as_view()),

    path('product/image/create/', CreateProductImage.as_view()),
    path('product/video/create/', CreateProductVideo.as_view()),
    path('product/document/create/', CreateProductDocument.as_view()),
    path('product/tag/create/', CreateProductTag.as_view()),
    path('product/specification/create/', CreateProductSpecification.as_view()),
    path('product/size/create/', CreateProductSize.as_view()),
    path('product/image/create/', CreateProductImage.as_view()),

    path('product/review/create/', CreateProductReview.as_view()),
    path('product/review/all/', ListProductReview.as_view()),
    path('product/review/<slug:id>/', UpdateProductReview.as_view()),
]