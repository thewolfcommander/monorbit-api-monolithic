from django.urls import path
from .views import *

app_name = 'premium'

urlpatterns = [
    path('membership/network/activity/all/', ListAllNetworkMembershipActivity.as_view(), name='network_membership_all'),
    path('membership/network/activity/create/', CreateNetworkMembershipActivity.as_view(), name='network_membership_create'),
    path('membership/network/subscription/create/', CreateNetworkMembershipSubscription.as_view(), name='network_subscription_create'),

    path('membership/network/billing/all/', ListNetworkBilling.as_view(), name='list_network_billing'),
    path('membership/network/billing/create/', CreateNetworkBilling.as_view(), name='create_network_billing'),
    path('membership/network/billing/update/<int:id>/', UpdateNetworkBilling.as_view(), name='update_network_billing'),

    path('membership/network/payment/enter/', CreateRZPOrder.as_view(), name='enter_network_payment'),
    path('membership/network/payment/verify/', PaymentVerification.as_view(), name='verify_network_payment'),
]