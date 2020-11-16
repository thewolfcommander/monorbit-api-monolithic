from rest_framework import generics, permissions

from .serializers import *
from .models import *


class ContactUsListCreateView(generics.ListCreateAPIView):
    serializer_class = ContactUsSerializer
    queryset = ContactUs.objects.all()
    permission_classes = [permissions.AllowAny]
    filterset_fields = [
        'email_or_phone',
        'is_email',
        'is_phone',
        'is_contacted',
        'created_at',
        'updated_at'
    ]


class ContactUsUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ContactUsSerializer
    queryset = ContactUs.objects.all()
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)