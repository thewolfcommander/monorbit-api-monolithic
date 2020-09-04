from rest_framework import generics, permissions

from .serializers import *
from .models import *


import logging
logger = logging.getLogger(__name__)


class ListCreateJobProfile(generics.ListCreateAPIView):
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
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = JobProfileSerializer
    queryset = JobProfile.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    
class ListCreateDeliveryBoyVehicle(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DeliveryBoyVehicleSerializer
    queryset = DeliveryBoyVehicle.objects.all()
    filterset_fields = [
        'delivery_boy',
        'type_of_vehicle',
        'active'
    ]


class UpdateDeliveryBoyVehicle(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DeliveryBoyVehicleSerializer
    queryset = DeliveryBoyVehicle.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    
class ListDeliveryBoys(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DeliveryBoyShowSerializer
    queryset = DeliveryBoy.objects.all()
    filterset_fields = [
        'job_profile',
        'is_recharged',
        'active'
    ]


class CreateDeliveryBoys(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DeliveryBoyCreateSerializer
    queryset = DeliveryBoy.objects.all()


class UpdateDeliveryBoy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DeliveryBoyShowSerializer
    queryset = DeliveryBoy.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ListPermanentEmployee(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PermanentEmployeeShowSerializer
    queryset = PermanentEmployee.objects.all()
    filterset_fields = [
        'job_profile',
        'is_recharged',
        'active'
    ]


class CreatePermanentEmployee(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PermanentEmployeeCreateSerializer
    queryset = PermanentEmployee.objects.all()


class UpdatePermanentEmployee(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PermanentEmployeeShowSerializer
    queryset = PermanentEmployee.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ListFreelancer(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FreelancerShowSerializer
    queryset = Freelancer.objects.all()
    filterset_fields = [
        'job_profile',
        'is_recharged',
        'active'
    ]


class CreateFreelancer(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FreelancerCreateSerializer
    queryset = Freelancer.objects.all()


class UpdateFreelancer(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FreelancerShowSerializer
    queryset = Freelancer.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)