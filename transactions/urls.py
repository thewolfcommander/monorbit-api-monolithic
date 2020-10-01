from django.urls import path
from .views import *

app_name = 'transactions'

urlpatterns = [
    path('network/followers/', ListNetworkFollowers.as_view(), name='list_network_followers'),
    path('network/followers/create/', CreateNetworkFollower.as_view(), name='create_network_followers'),
    path('network/followers/delete/<int:id>/', DeleteNetworkFollower.as_view(), name='delete_network_followers'),

    # Hiring Staff
    path('network/job-application/delivery-boys/all/', ListNetworkDeliveryBoyApplication.as_view(), name='list_db_job_application'),
    path('network/job-application/delivery-boys/create/', CreateNetworkDeliveryBoyApplication.as_view(), name='create_db_job_application'),
    path('network/job-application/delivery-boys/update/<int:id>/', UpdateNetworkDeliveryBoyApplication.as_view(), name='update_db_job_application'),

    path('network/job-application/permanent-employee/all/', ListNetworkPermanentEmployeeApplication.as_view(), name='list_pe_job_application'),
    path('network/job-application/permanent-employee/create/', CreateNetworkPermanentEmployeeApplication.as_view(), name='create_pe_job_application'),
    path('network/job-application/permanent-employee/update/<int:id>/', UpdateNetworkPermanentEmployeeApplication.as_view(), name='update_pe_job_application'),

    path('network/job-application/freelancer/all/', ListNetworkFreelancerApplication.as_view(), name='list_freelancer_job_application'),
    path('network/job-application/freelancer/create/', CreateNetworkFreelancerApplication.as_view(), name='create_freelancer_job_application'),
    path('network/job-application/freelancer/update/<int:id>/', UpdateNetworkFreelancerApplication.as_view(), name='update_freelancer_job_application'),
]