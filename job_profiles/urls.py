from django.urls import path

from .views import *


urlpatterns = [
    path('all/', ListCreateJobProfile.as_view()),
    path('update/<slug:id>/', UpdateJobProfile.as_view()),

    path('delivery-boy/vehicle/', ListCreateDeliveryBoyVehicle.as_view()),
    path('delivery-boy/vehicle/<slug:id>/', UpdateDeliveryBoyVehicle.as_view()),
    path('delivery-boy/all/', ListDeliveryBoys.as_view()),
    path('delivery-boy/create/', CreateDeliveryBoys.as_view()),
    path('delivery-boy/update/<slug:id>/', UpdateDeliveryBoy.as_view()),

    path('permanent/all/', ListPermanentEmployee.as_view()),
    path('permanent/create/', CreatePermanentEmployee.as_view()),
    path('permanent/update/<slug:id>/', UpdatePermanentEmployee.as_view()),

    path('freelancer/all/', ListFreelancer.as_view()),
    path('freelancer/create/', CreateFreelancer.as_view()),
    path('freelancer/update/<slug:id>/', UpdateFreelancer.as_view()),
]