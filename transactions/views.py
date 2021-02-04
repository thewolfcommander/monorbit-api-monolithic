from django.http import Http404
from rest_framework import generics, permissions
from rest_framework.views import Response

from .models import *
from .serializers import *
from .permissions import *


class CreateNetworkFollower(generics.CreateAPIView):
    """
    Here normal user can follow any network.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = NetworkFollower.objects.all()
    serializer_class = CreateNetworkFollowerSerializer


class ListNetworkFollowers(generics.ListAPIView):
    """
    List of all followers of a network.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = NetworkFollower.objects.all()
    serializer_class = ShowNetworkFollowerSerializer
    filterset_fields = [
        'network',
        'user',
        'network__name'
    ]


class DeleteNetworkFollower(generics.DestroyAPIView):
    """
    Normal user can unfollow network.
    """
    permission_classes = [permissions.IsAuthenticated,IsOwner]
    queryset = NetworkFollower.objects.all()
    serializer_class = ShowNetworkFollowerSerializer
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        try:
            # get networkfollower object using "id" 
            instance = self.get_object()
            # decrease user followed_networks by 1
            instance.user.followed_networks -= 1
            instance.user.save()
            # decrease network follower by 1
            instance.network.followers -= 1
            instance.network.save()
            self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=204)


class CreateNetworkDeliveryBoyApplication(generics.CreateAPIView):
    """
    Normal user can apply for delivery boy application on network job offerings.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = NetworkDeliveryBoyApplication.objects.all()
    serializer_class = CreateNetworkDeliveryBoyApplication


class ListNetworkDeliveryBoyApplication(generics.ListAPIView):
    """
    List of all delivery boy application on a job offering.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = NetworkDeliveryBoyApplication.objects.all()
    serializer_class = ShowNetworkDeliveryBoyApplication
    filterset_fields = [
        'offering',
        'delivery_boy',
        'application_status'
    ]


class UpdateNetworkDeliveryBoyApplication(generics.RetrieveUpdateDestroyAPIView):
    """
    Delivery boy who applied on job offering can update their application.
    """
    permission_classes = [permissions.IsAuthenticated,IsDeliveryApplicationOwner]
    queryset = NetworkDeliveryBoyApplication.objects.all()
    serializer_class = ShowNetworkDeliveryBoyApplication
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CreateNetworkPermanentEmployeeApplication(generics.CreateAPIView):
    """
    Normal user employee can apply for permanent employee application on network job offerings.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = NetworkPermanentEmployeeApplication.objects.all()
    serializer_class = CreateNetworkPermanentEmployeeApplication


class ListNetworkPermanentEmployeeApplication(generics.ListAPIView):
    """
    List of all permanent employee application on job offering (permanet employee job offering).
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = NetworkPermanentEmployeeApplication.objects.all()
    serializer_class = ShowNetworkPermanentEmployeeApplication
    filterset_fields = [
        'offering',
        'permanent_employee',
        'application_status'
    ]


class UpdateNetworkPermanentEmployeeApplication(generics.RetrieveUpdateDestroyAPIView):
    """
    User who applied to permanent employee job offering can update thier application.
    """
    permission_classes = [permissions.IsAuthenticated,IsPermanentEmployeeApplicationOwner]
    queryset = NetworkPermanentEmployeeApplication.objects.all()
    serializer_class = ShowNetworkPermanentEmployeeApplication
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CreateNetworkFreelancerApplication(generics.CreateAPIView):
    """
    Freelancer can apply for freelancer job offering.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = NetworkFreelancerApplication.objects.all()
    serializer_class = CreateNetworkFreelancerApplication


class ListNetworkFreelancerApplication(generics.ListAPIView):
    """
    List of all freelancers application on freelancer job offering.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = NetworkFreelancerApplication.objects.all()
    serializer_class = ShowNetworkFreelancerApplication
    filterset_fields = [
        'offering',
        'freelancer',
        'application_status'
    ]


class UpdateNetworkFreelancerApplication(generics.RetrieveUpdateDestroyAPIView):
    """
    Freelancer can update their application.
    """
    permission_classes = [permissions.IsAuthenticated,IsFreelancerApllicationOwner]
    queryset = NetworkFreelancerApplication.objects.all()
    serializer_class = ShowNetworkFreelancerApplication
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)