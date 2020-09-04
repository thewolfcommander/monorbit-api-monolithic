from django.urls import path

from .views import *

app_name='cart'

urlpatterns = [
    path('create/', CreateCart.as_view()),
    path('all/', ListCart.as_view()),
    path('detail/<slug:id>/', UpdateCart.as_view()),
    
    path('entry/product/create/', CreateProductEntry.as_view()),
    path('entry/product/all/', ListProductEntry.as_view()),
    path('entry/product/detail/<int:id>/', UpdateProductEntry.as_view()),
]