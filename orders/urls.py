from django.urls import path
from .views import *

app_name='orders'

urlpatterns = [
    path('create/', CreateOrder.as_view(), name='create'),
    path('all/', ListAllOrders.as_view(), name='all'),
    path('detail/<slug:id>/', OrderDetail.as_view(), name='detail'),
    path('update/<slug:id>/', UpdateOrder.as_view(), name='update'),
]