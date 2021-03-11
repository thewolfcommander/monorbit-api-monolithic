from rest_framework import generics, permissions, pagination

from .serializers import *
from .models import *

import logging
logger = logging.getLogger(__name__)


class FcmDevieAPIView(generics.CreateAPIView):
    serializer_class = FCMDeviceCreateSerializer
    queryset = FcmDevice.objects.all()
    permission_classes = []

class FcmDevieListAPIView(generics.ListAPIView):
    serializer_class = FCMDeviceCreateSerializer
    queryset = FcmDevice.objects.all()
    permission_classes = []

    filterset_fields = [
        'user'
    ]
