from rest_framework import generics, permissions

from .serializers import *
from .models import *
from .permissions import *


import logging
logger = logging.getLogger(__name__)


class ListCreateJobProfile(generics.ListCreateAPIView):
    """
    List of normal user's job profile.
    A user who is authenticated can create thier job profile.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = JobProfileSerializer
    queryset = JobProfile.objects.all()
    filterset_fields = [
        'user',
        'city',
        'state',
        'country',
        'pincode',
        'is_verified',
        'is_vehicle',
        'is_delivery_boy',
        'is_permanent_employee',
        'is_freelancer'
    ]


class UpdateJobProfile(generics.RetrieveUpdateDestroyAPIView):
    """
    Normal User can update(put,patch,delete) their own job profile.
    Other can see only thier detail.
    """
    permission_classes = [permissions.IsAuthenticated,JobProfilePermission]
    serializer_class = JobProfileSerializer
    queryset = JobProfile.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    
class ListCreateDeliveryBoyVehicle(generics.ListCreateAPIView):
    """
    List of Delivery boy vehicle.
    Delivery boy can create their vehicle. (What type of vehicle they have)
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DeliveryBoyVehicleSerializer
    queryset = DeliveryBoyVehicle.objects.all()
    filterset_fields = [
        'delivery_boy',
        'type_of_vehicle',
        'active'
    ]


class UpdateDeliveryBoyVehicle(generics.RetrieveUpdateDestroyAPIView):
    """
    Delivery boy can update their vehicle. (What type of vehicle they have)
    """
    permission_classes = [permissions.IsAuthenticated,DeliveryBoyVehiclePermission]
    serializer_class = DeliveryBoyVehicleSerializer
    queryset = DeliveryBoyVehicle.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    
class ListDeliveryBoys(generics.ListAPIView):
    """
    List of all delivery boys on monorbit.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DeliveryBoyShowSerializer
    queryset = DeliveryBoy.objects.all()
    filterset_fields = [
        'job_profile',
        'is_recharged',
        'active'
    ]


class CreateDeliveryBoys(generics.CreateAPIView):
    """
    Delivery boy create view (Who want to delivery boy job)
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DeliveryBoyCreateSerializer
    queryset = DeliveryBoy.objects.all()


class UpdateDeliveryBoy(generics.RetrieveUpdateDestroyAPIView):
    """
    Delivery boy update their details.
    """
    permission_classes = [permissions.IsAuthenticated,DeliveryBoyPermanentEmployeeAndFreelancer]
    serializer_class = DeliveryBoyShowSerializer
    queryset = DeliveryBoy.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ListPermanentEmployee(generics.ListAPIView):
    """
    List of permanent employee of a network.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PermanentEmployeeShowSerializer
    queryset = PermanentEmployee.objects.all()
    filterset_fields = [
        'job_profile',
        'is_recharged',
        'active'
    ]


class CreatePermanentEmployee(generics.CreateAPIView):
    """
    Create permanent employee job profile. (If user want permanent job)
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PermanentEmployeeCreateSerializer
    queryset = PermanentEmployee.objects.all()


class UpdatePermanentEmployee(generics.RetrieveUpdateDestroyAPIView):
    """
    User can update their permanent employee job profile.
    """
    permission_classes = [permissions.IsAuthenticated,DeliveryBoyPermanentEmployeeAndFreelancer]
    serializer_class = PermanentEmployeeShowSerializer
    queryset = PermanentEmployee.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ListFreelancer(generics.ListAPIView):
    """
    List of Freelancer.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FreelancerShowSerializer
    queryset = Freelancer.objects.all()
    filterset_fields = [
        'job_profile',
        'is_recharged',
        'active'
    ]


class CreateFreelancer(generics.CreateAPIView):
    """
    User can create their freelancer job profile.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FreelancerCreateSerializer
    queryset = Freelancer.objects.all()


class UpdateFreelancer(generics.RetrieveUpdateDestroyAPIView):
    """
    Freelancer can update their freelancer job profile details.
    """
    permission_classes = [permissions.IsAuthenticated,DeliveryBoyPermanentEmployeeAndFreelancer]
    serializer_class = FreelancerShowSerializer
    queryset = Freelancer.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)