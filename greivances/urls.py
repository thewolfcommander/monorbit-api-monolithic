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

    # Tickets
    path('help/tickets/categories/', ListCreateTicketCategory.as_view(), name='list_create_ticket_category'),
    path('help/tickets/categories/update/<int:id>/', UpdateTicketCategory.as_view(), name='update_ticket_category'),
    path('help/tickets/all/', ListTicket.as_view(), name='list_ticket'),
    path('help/tickets/create/', CreateTicket.as_view(), name='create_ticket'),
    path('help/tickets/react/', GiveTicketReaction.as_view(), name='react_on_ticket'),
    path('help/tickets/update/<slug:id>/', UpdateTicket.as_view(), name='update_ticket'),
    path('help/tickets/comments/', ListCreateTicketComment.as_view(), name='list_create_ticket_comment'),
    path('help/tickets/comments/react/', GiveTicketCommentReaction.as_view(), name='react_on_ticket_comment'),
    path('help/tickets/comments/update/<int:id>/', UpdateTicketComment.as_view(), name='update_ticket_comment'),
]