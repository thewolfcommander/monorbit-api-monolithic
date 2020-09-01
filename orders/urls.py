from django.urls import path
from .views import *

urlpatterns = [
    path('create/', CreateOrder.as_view()),
    path('all/', ListAllOrders.as_view()),
    path('detail/<slug:id>/', OrderDetail.as_view()),
    path('update/<slug:id>/', UpdateOrder.as_view()),
]