from django.urls import path

from .views import *


app_name = 'core'

urlpatterns = [
    path('tips-to-grow/', ListCreateTipToGrow.as_view(), name='list_create_tips_to_grow'),
    path('tips-to-grow/update/<int:id>/', UpdateTipToGrow.as_view(), name='update_tips_to_grow'),

    path('email/send/', SendEmail.as_view(), name='send_email'),
    path('email/all/', AllEmail.as_view(), name='all_email'),
]