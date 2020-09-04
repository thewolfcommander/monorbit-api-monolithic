from django.urls import path

from .views import *

app_name = 'network'

urlpatterns = [
    # Network Categories
    path('categories/', NetworkCategoryListCreateView.as_view(), name='network-categories'),
    path('categories/<int:id>/', NetworkCategoryDetailView.as_view(), name='network-category'),

    # Network Types
    path('types/', NetworkTypeListCreateView.as_view(), name='network-types'),
    path('types/<int:id>/', NetworkTypeDetailView.as_view(), name='network-type'),

    # Networks
    path('create/', NetworkCreateView.as_view(), name='create-network'),
    path('all/', NetworkListView.as_view(), name='all-networks'),
    path('detail/<slug:id>/', NetworkDetailView.as_view(), name='network-detail'),
    path('delete/<slug:id>/', NetworkDeleteView.as_view(), name='network-delete'),
    path('reviews/', ListNetworkReview.as_view(), name='all-reviews'),
    path('reviews/<slug:id>/', UpdateNetworkReview.as_view(), name='review-detail'),

    # Network Sub Parts
    path('create/image/', CreateNetworkImage.as_view(), name='create-network-image'),
    path('create/video/', CreateNetworkVideo.as_view(), name='create-network-image'),
    path('create/document/', CreateNetworkDocument.as_view(), name='create-network-image'),
    path('create/timing/', CreateNetworkOperationTiming.as_view(), name='create-network-image'),
    path('create/location/', CreateNetworkOperationLocation.as_view(), name='create-network-image'),
    path('create/review/', CreateNetworkReview.as_view(), name='create-network-review'),
]