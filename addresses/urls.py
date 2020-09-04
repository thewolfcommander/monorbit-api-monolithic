from django.urls import *

from .views import *

app_name = 'addresses'

urlpatterns = [
    path('address/create/', CreateAddress.as_view()),
    path('address/all/', ListAllAddresses.as_view()),
    path('address/update/<slug:id>/', UpdateAddress.as_view()),
]