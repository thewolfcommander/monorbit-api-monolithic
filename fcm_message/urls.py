from django.urls import path
from .views import *

app_name='fcm_message'

urlpatterns = [
    path('notifications/', FcmDevieAPIView.as_view(), name='fcm-notification'),
    path('notifications/all/',FcmDevieListAPIView.as_view(),name='all-notifications')
    
]