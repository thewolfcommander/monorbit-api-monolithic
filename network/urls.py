from django.urls import path

from .views import *

app_name = 'network'

urlpatterns = [
    # Network Categories
    path('categories/', NetworkCategoryListCreateView.as_view(), name='network_categories'),
    path('categories/<int:id>/', NetworkCategoryDetailView.as_view(), name='network_category'),

    # Network Types
    path('types/', NetworkTypeListCreateView.as_view(), name='network_types'),
    path('types/<int:id>/', NetworkTypeDetailView.as_view(), name='network_type'),

    # Networks
    path('find/', FindNetwork.as_view(), name='find_network'),
    path('create/', NetworkCreateView.as_view(), name='create_network'),
    path('all/', NetworkListView.as_view(), name='all_networks'),
    path('detail/<slug:urlid>/', NetworkDetailView.as_view(), name='network_detail'),
    path('delete/<slug:id>/', NetworkDeleteView.as_view(), name='network_delete'),
    path('reviews/', ListNetworkReview.as_view(), name='all_reviews'),
    path('reviews/<slug:id>/', UpdateNetworkReview.as_view(), name='review_detail'),

    # Network Sub Parts
    path('create/image/', CreateNetworkImage.as_view(), name='create_network_image'),
    path('create/video/', CreateNetworkVideo.as_view(), name='create_network_image'),
    path('create/document/', CreateNetworkDocument.as_view(), name='create_network_image'),
    path('create/timing/', CreateNetworkOperationTiming.as_view(), name='create_network_image'),
    path('create/location/', CreateNetworkOperationLocation.as_view(), name='create_network_image'),
    path('create/review/', CreateNetworkReview.as_view(), name='create_network_review'),

    # Network Jobs
    path('jobs/all/', ListNetworkJob.as_view(), name='list_network_jobs'),
    path('jobs/create/', CreateNetworkJob.as_view(), name='create_network_jobs'),
    path('jobs/detail/<slug:id>/', UpdateNetworkJob.as_view(), name='update_network_jobs'),
    path('jobs/offerings/all/', ListNetworkJobOffering.as_view(), name='list_network_job_offerings'),
    path('jobs/offerings/create/', CreateNetworkJobOffering.as_view(), name='create_network_job_offerings'),
    path('jobs/offerings/detail/<slug:id>/', UpdateNetworkJobOffering.as_view(), name='update_network_job_offerings'),

    # Staff
    path('staff/all/', ListNetworkStaff.as_view(), name='list_staff',),
    path('staff/create/', CreateNetworkStaff.as_view(), name='create_staff',),
    path('staff/detail/<slug:id>/', ShowNetworkStaff.as_view(), name='show_staff',),
    path('staff/update/<slug:id>/', UpdateNetworkStaff.as_view(), name='update_staff',),


    # Stats
    path('stats/all/', ShowNetworkStats.as_view(), name='list_stats'),
    path('stats/detail/<slug:network__urlid>/', NetworkStatDetail.as_view(), name='detail_stats'),


    # Options
    path('options/create/', CreateNetworkOption.as_view(), name='create_network_option'),
    path('options/all/', ListNetworkOption.as_view(), name='list_network_option'),
    path('options/update/<int:id>/', UpdateNetworkOption.as_view(), name='update_network_option'),
]