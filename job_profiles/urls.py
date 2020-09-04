from django.urls import path

from .views import *

app_name = 'job_profiles'

urlpatterns = [
    path('all/', ListCreateJobProfile.as_view(), name='all_profiles'),
    path('update/<slug:id>/', UpdateJobProfile.as_view(), name='update_profiles'),

    path('delivery-boy/vehicle/', ListCreateDeliveryBoyVehicle.as_view(), name='dboy_vehicle_all'),
    path('delivery-boy/vehicle/<slug:id>/', UpdateDeliveryBoyVehicle.as_view(), name='dboy_vehicle_update'),
    
    path('delivery-boy/all/', ListDeliveryBoys.as_view(), name='dboy_all'),
    path('delivery-boy/create/', CreateDeliveryBoys.as_view(), name='dboy_create'),
    path('delivery-boy/update/<slug:id>/', UpdateDeliveryBoy.as_view(), name='dboy_update'),

    path('permanent/all/', ListPermanentEmployee.as_view(), name='permanent_all'),
    path('permanent/create/', CreatePermanentEmployee.as_view(), name='permanent_create'),
    path('permanent/update/<slug:id>/', UpdatePermanentEmployee.as_view(), name='permanent_update'),

    path('freelancer/all/', ListFreelancer.as_view(), name='freelancer_all'),
    path('freelancer/create/', CreateFreelancer.as_view(), name='freelancer_create'),
    path('freelancer/update/<slug:id>/', UpdateFreelancer.as_view(), name='freelancer_update'),
]