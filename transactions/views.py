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