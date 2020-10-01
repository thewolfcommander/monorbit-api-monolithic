from django.http import Http404
from rest_framework import generics, permissions
from rest_framework.views import Response

from .models import *
from .serializers import *


class CreateNetworkFollower(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = NetworkFollower.objects.all()
    serializer_class = CreateNetworkFollowerSerializer


class ListNetworkFollowers(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = NetworkFollower.objects.all()
    serializer_class = ShowNetworkFollowerSerializer
    filterset_fields = [
        'network',
        'user',
        'network__name'
    ]


class DeleteNetworkFollower(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = NetworkFollower.objects.all()
    serializer_class = ShowNetworkFollowerSerializer
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.user.followed_networks -= 1
            instance.user.save()
            instance.network.followers -= 1
            instance.network.save()
            self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=204)


class CreateNetworkDeliveryBoyApplication(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = NetworkDeliveryBoyApplication.objects.all()
    serializer_class = CreateNetworkDeliveryBoyApplication


class ListNetworkDeliveryBoyApplication(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = NetworkDeliveryBoyApplication.objects.all()
    serializer_class = ShowNetworkDeliveryBoyApplication
    filterset_fields = [
        'offering',
        'delivery_boy',
        'application_status'
    ]


class UpdateNetworkDeliveryBoyApplication(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = NetworkDeliveryBoyApplication.objects.all()
    serializer_class = ShowNetworkDeliveryBoyApplication
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CreateNetworkPermanentEmployeeApplication(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = NetworkPermanentEmployeeApplication.objects.all()
    serializer_class = CreateNetworkPermanentEmployeeApplication


class ListNetworkPermanentEmployeeApplication(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = NetworkPermanentEmployeeApplication.objects.all()
    serializer_class = ShowNetworkPermanentEmployeeApplication
    filterset_fields = [
        'offering',
        'permanent_employee',
        'application_status'
    ]


class UpdateNetworkPermanentEmployeeApplication(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = NetworkPermanentEmployeeApplication.objects.all()
    serializer_class = ShowNetworkPermanentEmployeeApplication
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CreateNetworkFreelancerApplication(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = NetworkFreelancerApplication.objects.all()
    serializer_class = CreateNetworkFreelancerApplication


class ListNetworkFreelancerApplication(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = NetworkFreelancerApplication.objects.all()
    serializer_class = ShowNetworkFreelancerApplication
    filterset_fields = [
        'offering',
        'freelancer',
        'application_status'
    ]


class UpdateNetworkFreelancerApplication(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = NetworkFreelancerApplication.objects.all()
    serializer_class = ShowNetworkFreelancerApplication
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)