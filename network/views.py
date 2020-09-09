from rest_framework import generics, permissions
from rest_framework.views import APIView

from .models import *
from .serializers import *
from .permissions import *


import logging
logger = logging.getLogger(__name__)

class NetworkCategoryListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = NetworkCategory.objects.all()
    serializer_class = NetworkCategorySerializer
    filterset_fields = [
        'priority',
    ]


class NetworkCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = NetworkCategory.objects.all()
    serializer_class = NetworkCategorySerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class NetworkTypeListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = NetworkType.objects.all()
    serializer_class = NetworkTypeSerializer


class NetworkTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = NetworkType.objects.all()
    serializer_class = NetworkTypeSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    
class NetworkCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Network.objects.all()
    serializer_class = CreateNetworkSerializer


class NetworkListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Network.objects.all()
    serializer_class = ShowNetworkSerializer
    filterset_fields = [
        'user',
        'category',
        'network_type',
        'city',
        'state',
        'country',
        'pincode',
        'rating',
        'is_verified',
        'is_active',
        'is_spam',
        'is_video',
        'is_document',
        'is_archived',
    ]


class NetworkDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Network.objects.all()
    serializer_class = NetworkDetailSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    
class NetworkDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Network.objects.all()
    serializer_class = DeleteNetworkSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    
class CreateNetworkImage(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsSubPartOwner]
    queryset = NetworkImage.objects.all()
    serializer_class = NetworkImageCreateSerializer


class CreateNetworkVideo(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsSubPartOwner]
    queryset = NetworkVideo.objects.all()
    serializer_class = NetworkVideoCreateSerializer


class CreateNetworkDocument(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsSubPartOwner]
    queryset = NetworkDocument.objects.all()
    serializer_class = NetworkDocumentCreateSerializer


class CreateNetworkOperationTiming(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsSubPartOwner]
    queryset = NetworkOperationTiming.objects.all()
    serializer_class = NetworkOperationTimingCreateSerializer


class CreateNetworkOperationLocation(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsSubPartOwner]
    queryset = NetworkOperationLocation.objects.all()
    serializer_class = NetworkOperationLocationCreateSerializer


class CreateNetworkReview(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = NetworkReview.objects.all()
    serializer_class = NetworkReviewCreateSerializer


class ListNetworkReview(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = NetworkReview.objects.all()
    serializer_class = NetworkReviewShowSerializer
    filterset_fields = [
        'network',
        'by',
        'rating',
        'is_spam',
        'is_active'
    ]


class UpdateNetworkReview(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = NetworkReview.objects.all()
    serializer_class = NetworkReviewShowSerializer
    lookup_field = 'id'
