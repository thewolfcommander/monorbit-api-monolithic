from django.urls import path
from .views import *

app_name = 'premium'

urlpatterns = [
    path('membership/network/activity/all/', ListAllNetworkMembershipActivity.as_view(), name='network_membership_all'),
    path('membership/network/activity/create/', CreateNetworkMembershipActivity.as_view(), name='network_membership_create'),
]