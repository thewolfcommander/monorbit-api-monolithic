from django.urls import path
from .views import *

app_name = 'transactions'

urlpatterns = [
    path('network/followers/', ListNetworkFollowers.as_view(), name='list_network_followers'),
    path('network/followers/create/', CreateNetworkFollower.as_view(), name='create_network_followers'),
    path('network/followers/delete/<int:id>/', DeleteNetworkFollower.as_view(), name='delete_network_followers'),
]