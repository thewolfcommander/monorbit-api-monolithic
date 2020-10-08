from django.urls import path

from .views import *

app_name = 'greivances'

urlpatterns = [
    path('faqs/categories/', ListCreateFAQCategory.as_view(), name='list_create_faq_category'),
    path('faqs/categories/update/<int:id>/', UpdateFAQCategory.as_view(), name='update_faq_category'),
    path('faqs/create/', CreateFAQ.as_view(), name='create_faq'),
    path('faqs/all/', ListFAQ.as_view(), name='list_faq'),
    path('faqs/update/<slug:id>/', UpdateFAQ.as_view(), name='update_faq'),
    path('faqs/reactions/create/', CreateFAQReaction.as_view(), name='create_faq_reaction'),
    path('faqs/reactions/delete/<int:id>/', DeleteFAQReaction.as_view(), name='delete_faq_reaction'),
]