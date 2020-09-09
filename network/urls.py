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
    path('create/', NetworkCreateView.as_view(), name='create_network'),
    path('all/', NetworkListView.as_view(), name='all_networks'),
    path('detail/<slug:id>/', NetworkDetailView.as_view(), name='network_detail'),
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
]