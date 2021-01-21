import json

from rest_framework import generics, permissions
from rest_framework.views import APIView, Response
from rest_framework.serializers import ValidationError

from .models import *
from .serializers import *
from . import rzp


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
                raise ValidationError(detail="Plan Doesn't exists", code=404)
        except Network.DoesNotExist:
            raise ValidationError(detail="Network Doesn't exists", code=404)


class CreateNetworkBilling(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NetworkBillingCreateSerializer
    queryset = NetworkBilling.objects.all()


class ListNetworkBilling(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NetworkBillingShowSerializer
    queryset = NetworkBilling.objects.all()        
    filterset_fields = [
        'network',
        'network__user',
        'email',
        'city',
        'state',
        'pincode',
        'country',
        'is_active'
    ]


class UpdateNetworkBilling(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NetworkBillingShowSerializer
    queryset = NetworkBilling.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    

class CreateRZPOrder(APIView):
    # permission_classes =[permissions.IsAuthenticated]
    permission_classes =[permissions.AllowAny]

    def post(self, request, format=None):
        currency = 'INR'
        receipt = request.data.get('billing_profile')
        notes= request.data.get('notes')
        plan = request.data.get('plan')
        days = request.data.get('days')
        print(request.data)

        # base_amount = 0.85*days
        # tax = float(base_amount*0.18)    # Initially taking 18% GST
        # amount = float(base_amount) + float(tax)
        # order = rzp.create_order(
        #     order_currency=currency,
        #     order_amount=int(amount*100),
        #     order_reciept=receipt,
        #     notes=notes 
        # )
        # order_rec = NetworkMembershipOrderReciept.objects.create(
        #     # network = network,
        #     order_id = order["id"],
        #     entity = order["entity"],
        #     amount = order["amount"],
        #     amount_paid = order["amount_paid"],
        #     amount_due = order["amount_due"],
        #     currency = order["currency"],
        #     status = order["status"],
        #     attempts = order["attempts"],
        #     created_at_rzp = order["created_at"],
        # )
        # return Response({
        #     'status': True,
        #     'message': "Order Created Successfully",
        #     'order_rec': {
        #         # 'network' : network,
        #         'order_id' : order["id"],
        #         'entity' : order["entity"],
        #         'amount' : order["amount"],
        #         'amount_paid' : order["amount_paid"],
        #         'amount_due' : order["amount_due"],
        #         'currency' : order["currency"],
        #         'status' : order["status"],
        #         'attempts' : order["attempts"],
        #         'created_at_rzp' : order["created_at"],
        #     }
        # }, status=201)

        if plan is None:
            raise ValidationError(detail="Invalid Plan Details", code=400)

        if receipt is None:
            raise ValidationError(detail="Invalid Billing Profile", code=400)
        try:
            try:
                plan_obj = NetworkMembershipPlan.objects.get(name=plan)
                try:
                    billing_obj = NetworkBilling.objects.get(id=receipt)
                    base_amount = int(plan_obj.price_per_day) * int(days)
                    # base_amount = 1*days
                    tax = float(base_amount*0.18)    # Initially taking 18% GST
                    transaction_charge = float(base_amount*0.035)
                    amount = float(base_amount) + float(tax) + float(transaction_charge)
                    order = rzp.create_order(
                        order_currency=currency,
                        order_amount=int(amount*100),
                        order_reciept=str(receipt),
                        notes=notes
                    )
                    order_rec = NetworkMembershipOrderReciept.objects.create(
                        network = billing_obj.network,
                        order_id = order["id"],
                        entity = order["entity"],
                        amount = float(order["amount"])/100,
                        amount_paid = float(order["amount_paid"])/100,
                        amount_due = float(order["amount_due"])/100,
                        transaction_charge=round(float(transaction_charge), 2),
                        tax=round(float(tax), 2),
                        currency = order["currency"],
                        status = order["status"],
                        attempts = order["attempts"],
                        created_at_rzp = order["created_at"],
                    )
                    return Response({
                        'status': True,
                        'message': "Order Created Successfully",
                        'order_rec': {
                            'network' : billing_obj.network.id,
                            'order_id' : order["id"],
                            'entity' : order["entity"],
                            'amount' : order["amount"],
                            'amount_paid' : order["amount_paid"],
                            'amount_due' : order["amount_due"],
                            'transaction_charge': order_rec.transaction_charge,
                            'tax': order_rec.tax,
                            'currency' : order["currency"],
                            'status' : order["status"],
                            'attempts' : order["attempts"],
                            'created_at_rzp' : order["created_at"],
                        }
                    }, status=201)
                except NetworkBilling.DoesNotExist:
                    raise ValidationError(detail="Invalid Network Billing Information", code=404)
            except NetworkMembershipPlan.DoesNotExist:
                raise ValidationError(detail="Invalid Plan Detail", code=404)
        except Exception as e:
            raise ValidationError(detail="Subscription failed due to {}. Please try again later.".format(e), code=503)


class PaymentVerification(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        # print(request.data)
        # return Response({
        #     'status': 'ok'
        # })
        try:
            data = request.data
            try:
                order_receipt = NetworkMembershipOrderReciept.objects.get(order_id= data["payload"]["payment"]["entity"]["order_id"])
                order_receipt.amount_paid = float(data["payload"]["order"]["entity"]["amount"])/100
                order_receipt.amount_due = 0.00
                order_receipt.status = data["payload"]["order"]["entity"]["status"]
                order_receipt.status = data["payload"]["order"]["entity"]["attempts"]
                order_receipt.save()
            except NetworkMembershipOrderReciept.DoesNotExist:
                order_receipt = None
            try:
                NetworkMembershipPaymentInvoice.objects.get(
                    account_id = data["account_id"],
                    payment_id = data["payload"]["payment"]["entity"]["id"],
                    order_id = data["payload"]["payment"]["entity"]["order_id"]
                )
            except NetworkMembershipPaymentInvoice.DoesNotExist:
                payment_invoice = NetworkMembershipPaymentInvoice.objects.create(
                    account_id = data["account_id"],
                    payment_id = data["payload"]["payment"]["entity"]["id"],
                    order_id = data["payload"]["payment"]["entity"]["order_id"],
                    network_order_receipt=order_receipt
                )
        except Exception as e:
            pass
        return Response({
            'status': 'ok'
        }, status=200)


class CreateNetworkMembershipSubscription(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        billing_profile = request.data.get('billing_profile', None)
        plan = request.data.get('plan', None)
        network_order_receipt = request.data.get('network_order_receipt', None)

        if billing_profile is None:
            raise ValidationError(detail="Please provide Billing Profile", code=400)

        if plan is None:
            raise ValidationError(detail="Please provide plan details", code=400)
        
        if network_order_receipt is None:
            raise ValidationError(detail="Please provide network membership order receipt", code=400)

        try:
            billing_obj = NetworkBilling.objects.get(id=billing_profile)
            try:
                plan_obj = NetworkMembershipPlan.objects.get(id=plan)
                try:
                    order_receipt = NetworkMembershipOrderReciept.objects.get(id=network_order_receipt)
                    payment = order_receipt.amount_paid
                    try:
                        relation = NetworkMembershipRelation.objects.get(network=billing_obj.network)
                        try:
                            activity = NetworkMembershipActivity.objects.get(relation=relation)
                            activity.relation.plan = plan_obj
                            activity.relation.save()
                            instance = NetworkMembershipSubscription.objects.create(
                                activity=activity,
                                billing_profile=billing_obj,
                                network_order_receipt=order_receipt,
                                payment=payment
                            )
                            invoice = NetworkMembershipInvoice.objects.create(subscription=instance)
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
                                    "billing_profile": instance.billing_profile,
                                    "network_order_receipt": instance.network_order_receipt,
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
                            activity = NetworkMembershipActivity.objects.create(
                                relation=relation
                            )
                            instance = NetworkMembershipSubscription.objects.create(
                                activity=activity,
                                billing_profile=billing_obj,
                                network_order_receipt=order_receipt,
                                payment=payment
                            )
                            invoice = NetworkMembershipInvoice.objects.create(subscription=instance)
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
                                    "billing_profile": instance.billing_profile,
                                    "network_order_receipt": instance.network_order_receipt,
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
                        relation = NetworkMembershipRelation.objects.create(
                            network=billing_obj.network,
                            plan=plan_obj
                        )
                        activity = NetworkMembershipActivity.objects.create(
                            relation=relation
                        )
                        instance = NetworkMembershipSubscription.objects.create(
                            activity=activity,
                            billing_profile=billing_obj,
                            network_order_receipt=order_receipt,
                            payment=payment
                        )
                        invoice = NetworkMembershipInvoice.objects.create(subscription=instance)
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
                                "billing_profile": instance.billing_profile,
                                "network_order_receipt": instance.network_order_receipt,
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
                except NetworkMembershipOrderReciept.DoesNotExist:
                    raise ValidationError(detail="Invalid Order Receipt. Please try again with correct receipt", code=404)
            except NetworkMembershipPlan.DoesNotExist:
                raise ValidationError(detail="Invalid Plan ID. Please try again with correct plan", code=404)
        except NetworkBilling.DoesNotExist:
            raise ValidationError(detail="Invalid Billing Profile. Please try again with correct profile", code=404)