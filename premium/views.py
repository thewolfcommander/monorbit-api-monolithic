from rest_framework import generics, permissions
from rest_framework.views import APIView, Response

from .models import *
from .serializers import *
from .rzp import client, create_order


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
        'trial_active_till'
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


class CreateRZPOrder(APIView):
    permission_classes =[permissions.IsAuthenticated]

    def post(self, request, format=None):
        currency = 'INR'
        pass


class CreateNetworkMembershipSubscription(APIView):
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
                        activity = NetworkMembershipActivity.objects.get(relation=relation)
                        activity.relation.plan = plan
                        activity.relation.save()
                        instance = NetworkMembershipSubscription.objects.create(
                            activity = activity,
                            payment=payment
                        )
                        invoice = NetworkMembershipInvoice.objects.create(subscription=instance)
                        order = create_order(
                            order_currency='INR',
                            order_amount=int(payment*100),
                            order_reciept=invoice.id,
                            notes={
                                "subscription": instance.id,
                                "network": network.name
                            }
                        )
                        instance.payment_order_id = order['id']
                        instance.save()
                        return Response(data={
                            "status": True,
                            "message": "Successfully created a subscription",
                            "activity": {
                                "id": str(activity.id),
                                "plan": {
                                    "name": activity.relation.plan.name,
                                    "price_per_day": activity.relation.plan.price_per_day
                                },
                                "network": {
                                    "id": activity.relation.network.id,
                                    "name": activity.relation.network.name,
                                    "is_premium": activity.relation.network.is_premium
                                },
                                "created": activity.created,
                                "trial_expiry": activity.trial_expiry,
                                "trial_active_till": activity.trial_active_till,
                                "trial_applied": activity.trial_applied,
                                "active": activity.active
                            },
                            "subscription": {
                                "id": instance.id,
                                "payment_order_id": instance.payment_order_id,
                                "payment": instance.payment,
                                "started": instance.started,
                                "is_trial": instance.is_trial,
                                "expiry": instance.expiry,
                                "active_till": instance.active_till,
                                "active": instance.active
                            },
                            "invoice": {
                                "id": invoice.id,
                                "invoice_description": invoice.invoice_description,
                                "invoice_period_start_date": invoice.invoice_period_start_date,
                                "invoice_period_end_date": invoice.invoice_period_end_date,
                                "invoice_amount": invoice.invoice_amount,
                                "is_paid": invoice.is_paid,
                                "invoice_created": invoice.invoice_created,
                            }
                        }, status=200)
                    except NetworkMembershipActivity.DoesNotExist:
                        activity = instance = NetworkMembershipActivity.objects.create(
                            relation=relation
                        )
                        instance = NetworkMembershipSubscription.objects.create(
                            activity = activity,
                            payment_order_id=order_id,
                            payment=payment
                        )
                        invoice = NetworkMembershipInvoice.objects.create(subscription=instance, is_paid=True)
                        order = create_order(
                            order_currency='INR',
                            order_amount=int(payment*100),
                            order_reciept=invoice.id,
                            notes={
                                "subscription": instance.id,
                                "network": network.name
                            }
                        )
                        instance.payment_order_id = order['id']
                        instance.save()
                        return Response(data={
                            "status": True,
                            "message": "Successfully created a subscription",
                            "activity": {
                                "id": str(activity.id),
                                "plan": {
                                    "name": activity.relation.plan.name,
                                    "price_per_day": activity.relation.plan.price_per_day
                                },
                                "network": {
                                    "id": activity.relation.network.id,
                                    "name": activity.relation.network.name,
                                    "is_premium": activity.relation.network.is_premium
                                },
                                "created": activity.created,
                                "trial_expiry": activity.trial_expiry,
                                "trial_active_till": activity.trial_active_till,
                                "trial_applied": activity.trial_applied,
                                "active": activity.active
                            },
                            "subscription": {
                                "id": instance.id,
                                "payment_order_id": instance.payment_order_id,
                                "payment": instance.payment,
                                "started": instance.started,
                                "is_trial": instance.is_trial,
                                "expiry": instance.expiry,
                                "active_till": instance.active_till,
                                "active": instance.active
                            },
                            "invoice": {
                                "id": invoice.id,
                                "invoice_description": invoice.invoice_description,
                                "invoice_period_start_date": invoice.invoice_period_start_date,
                                "invoice_period_end_date": invoice.invoice_period_end_date,
                                "invoice_amount": invoice.invoice_amount,
                                "is_paid": invoice.is_paid,
                                "invoice_created": invoice.invoice_created,
                            }
                        }, status=200)
                except NetworkMembershipRelation.DoesNotExist:
                    relation = NetworkMembershipRelation.objects.create(network=network, plan=plan)
                    activity = instance = NetworkMembershipActivity.objects.create(
                            relation=relation
                        )
                    instance = NetworkMembershipSubscription.objects.create(
                        activity = activity,
                        payment_order_id=order_id,
                        payment=payment
                    )
                    invoice = NetworkMembershipInvoice.objects.create(subscription=instance, is_paid=True)
                    order = create_order(
                            order_currency='INR',
                            order_amount=int(payment*100),
                            order_reciept=invoice.id,
                            notes={
                                "subscription": instance.id,
                                "network": network.name
                            }
                        )
                    instance.payment_order_id = order.id
                    instance.save()
                    return Response(data={
                        "status": True,
                        "message": "Successfully created a subscription",
                        "activity": {
                            "id": str(activity.id),
                            "plan": {
                                "name": activity.relation.plan.name,
                                "price_per_day": activity.relation.plan.price_per_day
                            },
                            "network": {
                                "id": activity.relation.network.id,
                                "name": activity.relation.network.name,
                                "is_premium": activity.relation.network.is_premium
                            },
                            "created": activity.created,
                            "trial_expiry": activity.trial_expiry,
                            "trial_active_till": activity.trial_active_till,
                            "trial_applied": activity.trial_applied,
                            "active": activity.active
                        },
                        "subscription": {
                            "id": instance.id,
                            "payment_order_id": instance.payment_order_id,
                            "payment": instance.payment,
                            "started": instance.started,
                            "is_trial": instance.is_trial,
                            "expiry": instance.expiry,
                            "active_till": instance.active_till,
                            "active": instance.active
                        },
                        "invoice": {
                            "id": invoice.id,
                            "invoice_description": invoice.invoice_description,
                            "invoice_period_start_date": invoice.invoice_period_start_date,
                            "invoice_period_end_date": invoice.invoice_period_end_date,
                            "invoice_amount": invoice.invoice_amount,
                            "is_paid": invoice.is_paid,
                            "invoice_created": invoice.invoice_created,
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