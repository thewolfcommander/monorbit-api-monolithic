from rest_framework import generics, permissions
from rest_framework.views import APIView, Response

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


class FindNetwork(APIView):
    permission_classes = [permissions.AllowAny,]

    def post(self, request, format=None):
        username = request.data.get('username', None)

        if username is None:
            return Response({
                'status': False,
                'message': "Username not available"
            }, status=400)

        try:
            instance = Network.objects.get(urlid=username)
            return Response({
                'status': False,
                'message': "Username not available"
            }, status=400)
        except Network.DoesNotExist:
            return Response({
                'status': True,
                'message': 'Username available'
            }, status=200)
            
        return Response({
                'status': False,
                'message': "Username not available"
            }, status=400)




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
    lookup_field = 'urlid'

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
    queryset = NetworkReview.objects.all().order_by('-created')
    serializer_class = NetworkReviewShowSerializer
    filterset_fields = [
        'network',
        'by',
        'rating',
        'is_spam',
        'is_active'
    ]


class UpdateNetworkReview(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = NetworkReview.objects.all()
    serializer_class = NetworkReviewShowSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CreateNetworkJob(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = NetworkJob.objects.all()
    serializer_class = NetworkJobCreateSerializer


class ListNetworkJob(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = NetworkJob.objects.all().order_by('-updated')
    serializer_class = NetworkJobShowSerializer
    filterset_fields = [
        'network',
        'job_name',
        'job_type',
        'salary_payout_type',
        'age_bar_upper',
        'age_bar_lower',
        'is_verified',
        'is_vacant',
        'is_spam',
        'is_active'
    ]


class UpdateNetworkJob(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = NetworkJob.objects.all()
    serializer_class = NetworkJobShowSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    

class CreateNetworkJobOffering(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = NetworkJobOffering.objects.all()
    serializer_class = NetworkJobOfferingCreateSerializer


class ListNetworkJobOffering(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = NetworkJobOffering.objects.all().order_by('-updated')
    serializer_class = NetworkJobOfferingShowSerializer
    filterset_fields = [
        'job',
        'job__job_name',
        'job__job_type',
        'is_active',
        'is_filled',
        'max_staff_for_job',
        'last_date',
    ]


class UpdateNetworkJobOffering(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = NetworkJobOffering.objects.all()
    serializer_class = NetworkJobOfferingShowSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CreateNetworkStaff(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = NetworkStaff.objects.all()
    serializer_class = NetworkStaffCreateSerializer


class ListNetworkStaff(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = NetworkStaff.objects.all().order_by('-updated')
    serializer_class = NetworkStaffShowSerializer
    filterset_fields = [
        'job',
        'job__job_name',
        'job__job_type',
        'is_active',
        'application_id',
        'promoted_count',
        'demoted_count',
        'employee_score'
    ]


class ShowNetworkStaff(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = NetworkStaff.objects.all().order_by('-updated')
    serializer_class = NetworkStaffShowSerializer
    lookup_field = 'id'


class UpdateNetworkStaff(generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = NetworkStaff.objects.all()
    serializer_class = NetworkStaffUpdateSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)