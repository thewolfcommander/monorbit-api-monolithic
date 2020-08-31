from django.urls import path
from .views import *

urlpatterns = [
    path('create/', CreateOrder.as_view()),
]