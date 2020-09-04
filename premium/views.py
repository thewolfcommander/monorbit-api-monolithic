from rest_framework import generics, permissions
from rest_framework.views import APIView, Response

from .models import *
from .serializers import *


import logging
logger = logging.getLogger(__name__)

class ListAllNetworkMembershipActivity(generics.ListAPIView):
    queryset = NetworkMembershipActivity.objects.all()
    serializer_class = NetworkMembershipActivityShowSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = [
        'relation',
        'relation__network',
        'relation__plan',
        'active',
        'active_till'
    ]


class CreateNetworkMembershipActivity(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        network = request.data.get('network')
        plan = request.data.get('plan')
        payment = request.data.get('payment')

        try:
            network = Network.objects.get(id=network, is_active=True)
            try:
                plan = NetworkMembershipPlan.objects.get(name=str(plan))
                try:
                    relation = NetworkMembershipRelation.objects.get(network=network)
                    try:
                        instance = NetworkMembershipActivity.objects.get(relation=relation)
                        instance.relation.plan = plan
                        instance.relation.save()
                        instance.payment = float(payment)
                        instance.save()
                        return Response(data={
                            "status": True,
                            "message": "Successfully subscribed",
                            "activity": {
                                "id": str(instance.id),
                                "plan": {
                                    "name": instance.relation.plan.name,
                                    "price_per_day": instance.relation.plan.price_per_day
                                },
                                "network": {
                                    "id": instance.relation.network.id,
                                    "name": instance.relation.network.name,
                                    "is_premium": instance.relation.network.is_premium
                                },
                                "payment": instance.payment,
                                "expiry": instance.expiry,
                                "active_till": instance.active_till,
                                "active": instance.active
                            }
                        }, status=200)
                    except NetworkMembershipActivity.DoesNotExist:
                        instance = NetworkMembershipActivity.objects.create(
                            relation=relation,
                            payment = float(payment)
                        )
                        return Response(data={
                            "status": True,
                            "message": "Successfully subscribed",
                            "activity": {
                                "id": str(instance.id),
                                "plan": {
                                    "name": instance.relation.plan.name,
                                    "price_per_day": instance.relation.plan.price_per_day
                                },
                                "network": {
                                    "id": instance.relation.network.id,
                                    "name": instance.relation.network.name,
                                    "is_premium": instance.relation.network.is_premium
                                },
                                "payment": instance.payment,
                                "expiry": instance.expiry,
                                "active_till": instance.active_till,
                                "active": instance.active
                            }
                        }, status=200)
                except NetworkMembershipRelation.DoesNotExist:
                    relation = NetworkMembershipRelation.objects.create(network=network, plan=plan)
                    instance = NetworkMembershipActivity.objects.create(
                            relation=relation,
                            payment = float(payment)
                        )
                    return Response(data={
                            "status": True,
                            "message": "Successfully subscribed",
                            "activity": {
                                "id": str(instance.id),
                                "plan": {
                                    "name": instance.relation.plan.name,
                                    "price_per_day": instance.relation.plan.price_per_day
                                },
                                "network": {
                                    "id": instance.relation.network.id,
                                    "name": instance.relation.network.name,
                                    "is_premium": instance.relation.network.is_premium
                                },
                                "payment": instance.payment,
                                "expiry": instance.expiry,
                                "active_till": instance.active_till,
                                "active": instance.active
                            }
                    }, status=200)
            except NetworkMembershipPlan.DoesNotExist:
                return Response(data={
                    "status": False,
                    "message": "Plan Doesn't exists"
                }, status=400)
        except Network.DoesNotExist:
            return Response(data={
                "status": False,
                "message": "Network Doesn't exists"
            }, status=400)