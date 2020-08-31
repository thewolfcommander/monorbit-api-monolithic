from rest_framework import generics, permissions

from .models import *
from .serializers import *


class CreateOrder(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]