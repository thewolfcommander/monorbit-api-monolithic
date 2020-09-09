from django.urls import *

from .views import *

app_name = 'addresses'

urlpatterns = [
    path('address/create/', CreateAddress.as_view(), name='create'),
    path('address/all/', ListAllAddresses.as_view(), name='all'),
    path('address/update/<slug:id>/', UpdateAddress.as_view(), name='update'),
]