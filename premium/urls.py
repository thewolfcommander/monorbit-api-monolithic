from django.urls import path
from .views import *

app_name = 'premium'

urlpatterns = [
    path('membership/network/activity/all/', ListAllNetworkMembershipActivity.as_view()),
    path('membership/network/activity/create/', CreateNetworkMembershipActivity.as_view()),
]