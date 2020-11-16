from django.urls import path
from .views import *

app_name = 'adminer'

urlpatterns = [
    path('contacts/', ContactUsListCreateView.as_view(), name='list_create_contacts'),
    path('contacts/detail/<slug:id>/', ContactUsUpdateView.as_view(), name='update_contacts'),
]