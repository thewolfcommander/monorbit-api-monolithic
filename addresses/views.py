from rest_framework import generics, permissions

from .models import *
from .serializers import *

import logging
logger = logging.getLogger(__name__)

class CreateAddress(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Address.objects.all()
    serializer_class = AddressCreateSerializer


class ListAllAddresses(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Address.objects.all()
    serializer_class = AddressShowSerializer
    filterset_fields = [
        'user',
        'name',
        'landmark',
        'city',
        'state',
        'country',
        'pincode',
        'lat',
        'lng',
        'is_default',
        'is_active',
        'is_archived',
    ]


class UpdateAddress(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Address.objects.all()
    serializer_class = AddressShowSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)