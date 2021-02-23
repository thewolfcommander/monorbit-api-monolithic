from rest_framework import generics, permissions
from rest_framework.views import APIView, Response
from rest_framework.serializers import ValidationError

from .models import *
from .serializers import *
from .permissions import *


import logging
logger = logging.getLogger(__name__)

class NetworkCategoryListCreateView(generics.ListCreateAPIView):
    """
    Only admin can create network category. And provide list of network category to user who want to create their network.
    Network category such as "Food", "Footwear" etc.
    """
    permission_classes = [NetworkAdminPermission]
    queryset = NetworkCategory.objects.all()
    serializer_class = NetworkCategorySerializer
    filterset_fields = [
        'priority',
    ]


class NetworkCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Only Admin can Update Network Category.
    """
    permission_classes = [NetworkDetailAdminPermission]
    queryset = NetworkCategory.objects.all()
    serializer_class = NetworkCategorySerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class NetworkTypeListCreateView(generics.ListCreateAPIView):
    """
    Only admin can create network type. And provide list of network type to user who want to create their network.
    Network type such as "wholeseller", "retailer" etc.
    """
    permission_classes = [NetworkAdminPermission]
    queryset = NetworkType.objects.all()
    serializer_class = NetworkTypeSerializer


class NetworkTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Only Admin can Update Network type.
    """
    permission_classes = [NetworkDetailAdminPermission]
    queryset = NetworkType.objects.all()
    serializer_class = NetworkTypeSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    
class NetworkCreateView(generics.CreateAPIView):
    """
    A authenticated user can create their network and start thier bussiness here.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Network.objects.all()
    serializer_class = CreateNetworkSerializer


class FindNetwork(APIView):
    """
    Anyone can find network (search for network), if they have username(urlid) of network.
    """
    permission_classes = [permissions.AllowAny,]

    def post(self, request, format=None):
        username = request.data.get('username', None)

        if username is None:
            raise ValidationError(detail="Username not available", code=400)
        try:
            instance = Network.objects.get(urlid=username)
            raise ValidationError(detail="Username not available", code=400)
        except Network.DoesNotExist:
            return Response({
                'status': True,
                'message': 'Username available'
            }, status=200)
            
        raise ValidationError(detail="Username not available", code=400)


class ShowNetworkStats(generics.ListAPIView):
    """
    Stats (Analytics of network). In which network owner can see total orders, total sells etc.
    """
    permission_classes = [permissions.IsAuthenticated]
    # queryset = NetworkStat.objects.all().order_by('-updated')
    serializer_class = NetworkStatShowSerializer

    def get_queryset(self,*args,**kwargs):
        return NetworkStat.objects.filter(network__user=self.request.user)

    filterset_fields = [
        'network',
    ]


class NetworkStatDetail(generics.RetrieveAPIView):
    """
    Single Stats (Analytic of network). In which network owner can see total orders, total sells etc.
    """
    permission_classes = [permissions.IsAuthenticated,IsSubPartOwner]
    queryset = NetworkStat.objects.all().order_by('-updated')
    serializer_class = NetworkStatShowSerializer
    lookup_field = 'network__urlid'


class NetworkListView(generics.ListAPIView):
    """
    List of all network.
    """
    permission_classes = [permissions.AllowAny]
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
    """
    Network owner can update their network. (Delete permanently)
    """
    permission_classes = [permissions.AllowAny, IsOwnerOrReadOnly]
    queryset = Network.objects.all()
    serializer_class = NetworkDetailSerializer
    lookup_field = 'urlid'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    
class NetworkDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    Network owner can update their network. (delete temporary => is_active=False or is_archieved=False)
    """
    permission_classes = [permissions.AllowAny, IsOwnerOrReadOnly]
    queryset = Network.objects.all()
    serializer_class = DeleteNetworkSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    
class CreateNetworkImage(generics.CreateAPIView):
    """
    Network owner can create an image for thier network.
    """
    permission_classes = [permissions.AllowAny, IsSubPartOwner]
    queryset = NetworkImage.objects.all()
    serializer_class = NetworkImageCreateSerializer


class UpdateNetworkImage(generics.RetrieveUpdateDestroyAPIView):
    """
    Network owner can update an image for thier network.
    """
    permission_classes = [permissions.AllowAny]
    queryset = NetworkImage.objects.all()
    serializer_class = NetworkImageCreateSerializer
    lookup_field = 'id'

    def patch(self,request,*args,**kwargs):
        return self.partial_update(request,*args,**kwargs)



class CreateNetworkVideo(generics.CreateAPIView):
    """
    Network owner can create video for thier network.
    """
    permission_classes = [permissions.AllowAny, IsSubPartOwner]
    queryset = NetworkVideo.objects.all()
    serializer_class = NetworkVideoCreateSerializer


class CreateNetworkDocument(generics.CreateAPIView):
    """
    Network owner can upload document(pamplet, parcha etc) of their network.
    """
    permission_classes = [permissions.AllowAny, IsSubPartOwner]
    queryset = NetworkDocument.objects.all()
    serializer_class = NetworkDocumentCreateSerializer


class CreateNetworkOperationTiming(generics.CreateAPIView):
    """
    Network owner can decide timing of network.
    """
    permission_classes = [permissions.AllowAny, IsSubPartOwner]
    queryset = NetworkOperationTiming.objects.all()
    serializer_class = NetworkOperationTimingCreateSerializer


class CreateNetworkOperationLocation(generics.CreateAPIView):
    """
    Network owner can decide where(location) they are able to deliver thier product and services.
    """
    permission_classes = [permissions.AllowAny, IsSubPartOwner]
    queryset = NetworkOperationLocation.objects.all()
    serializer_class = NetworkOperationLocationCreateSerializer


class CreateNetworkReview(generics.CreateAPIView):
    """
    Normal user can review and rate any network based on their product and services.
    """
    permission_classes = [permissions.IsAuthenticated,]
    queryset = NetworkReview.objects.all()
    serializer_class = NetworkReviewCreateSerializer


class ListNetworkReview(generics.ListAPIView):
    """
    List of all review and rating of network.
    """
    permission_classes = [permissions.AllowAny,]
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
    """
    Normal user who has reviewed any network, can update the review and rating.
    """
    permission_classes = [IsSubPartOwner]
    queryset = NetworkReview.objects.all()
    serializer_class = NetworkReviewShowSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CreateNetworkJob(generics.CreateAPIView):
    """
    Network owner can create jobs if their network need any manpower.
    """
    permission_classes = [permissions.IsAuthenticated,]
    queryset = NetworkJob.objects.all()
    serializer_class = NetworkJobCreateSerializer


class ListNetworkJob(generics.ListAPIView):
    """
    List of all network jobs.
    """
    permission_classes = [permissions.AllowAny,]
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
    """
    Network owner can update their jobs of network.
    """
    permission_classes = [IsSubPartOwner]
    queryset = NetworkJob.objects.all()
    serializer_class = NetworkJobShowSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    

class CreateNetworkJobOffering(generics.CreateAPIView):
    """
    Normal user can offer a job.
    """
    permission_classes = [permissions.IsAuthenticated,]
    queryset = NetworkJobOffering.objects.all()
    serializer_class = NetworkJobOfferingCreateSerializer


class ListNetworkJobOffering(generics.ListAPIView):
    """
    List of job offerings by normal users.
    """
    permission_classes = [permissions.AllowAny,]
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
    """
    Normal user who has created job offering can update their job offering.
    """
    permission_classes = [permissions.IsAuthenticated,IsSubSubPartOwner]
    queryset = NetworkJobOffering.objects.all()
    serializer_class = NetworkJobOfferingShowSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CreateNetworkStaff(generics.CreateAPIView):
    """
    Network owner can create network staff, so that they can manage their staff.
    """
    permission_classes = [permissions.IsAuthenticated,]
    queryset = NetworkStaff.objects.all()
    serializer_class = NetworkStaffCreateSerializer


class ListNetworkStaff(generics.ListAPIView):
    """
    List of network staffs.
    """
    permission_classes = [permissions.AllowAny,]
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
    """
    Show single network staff.
    """
    permission_classes = [permissions.AllowAny,]
    queryset = NetworkStaff.objects.all().order_by('-updated')
    serializer_class = NetworkStaffShowSerializer
    lookup_field = 'id'


class UpdateNetworkStaff(generics.UpdateAPIView, generics.DestroyAPIView):
    """
    Network owner can update network staff(manage their staff).
    """
    permission_classes = [permissions.IsAuthenticated,IsSubSubPartOwner]
    queryset = NetworkStaff.objects.all()
    serializer_class = NetworkStaffUpdateSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)



class CreateNetworkOption(generics.CreateAPIView):
    """
    Network other details. (privacy purpose)
    """
    permission_classes = [permissions.IsAuthenticated,]
    queryset = NetworkOption.objects.all()
    serializer_class = NetworkOptionShowSerializer


class ListNetworkOption(generics.ListAPIView):
    """
    List of network option.
    """
    permission_classes = [permissions.AllowAny,]
    queryset = NetworkOption.objects.all()
    serializer_class = NetworkOptionShowSerializer
    filterset_fields = [
        'network',
        'network__urlid',
        'network__user__id',
        'network__user__mobile_number',
        'is_kyc',
        'is_special_user',
        'is_backer',
        'is_address_private',
        'is_phone_and_email_private'
    ]


class UpdateNetworkOption(generics.RetrieveUpdateDestroyAPIView):
    """
    Network owner can update their network option.
    """
    permission_classes = [permissions.IsAuthenticated,IsSubPartOwner]
    queryset = NetworkOption.objects.all()
    serializer_class = NetworkOptionShowSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


