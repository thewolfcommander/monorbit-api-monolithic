from rest_framework import generics, permissions

from .models import *
from .serializers import *
from accounts.permissions import IsOwner

import logging
logger = logging.getLogger(__name__)

class CreateAddress(generics.CreateAPIView):
    """
    View for Create addresses of users. 
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Address.objects.all()
    serializer_class = AddressCreateSerializer


class ListAllAddresses(generics.ListAPIView):
    """
    List of all addresses of users.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Address.objects.all()
    serializer_class = AddressShowSerializer
    filterset_fields = [
        'user',
        'name',
        'alt_name',
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
    """
    Address update( put,patch and delete) views. User, who created address can updated their own address.
    Anyone can get address (If authenticated).
    """
    permission_classes = [permissions.IsAuthenticated,IsOwner]
    queryset = Address.objects.all()
    serializer_class = AddressShowSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)