from rest_framework import generics, permissions
from rest_framework.views import APIView, Response
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.exceptions import ParseError

from .models import *
from .serializers import *

from monorbit.utils import mail, upload, files


class ListCreateTipToGrow(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TipToGrowSerializer
    queryset = TipToGrow.objects.all()
    filterset_fields = ["upvotes", "downvotes", "active"]


class GetARandomTip(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            random_tip = TipToGrow.objects.random()
            data = {
                "status": True,
                "message": "Here is a beautiful tip for you",
                "tip": random_tip.tip,
                "upvotes": random_tip.upvotes,
                "downvotes": random_tip.downvotes,
                "active": random_tip.active,
            }
            status = 200
        except:
            data = {"status": False, "message": "Sorry, cannot get a tip for you."}
            status = 503
        return Response(data=data, status=status)


class UpdateTipToGrow(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TipToGrowSerializer
    queryset = TipToGrow.objects.all()
    lookup_field = "id"

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class SendEmail(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        from_email = request.data.get("from_email", "support@monorbit.com")
        email_type = request.data.get("email_type")
        to_email = request.data.get("to_email")
        subject = request.data.get("subject")
        message = request.data.get("message")
        client_address = request.META["HTTP_X_FORWARDED_FOR"]
        failed = False
        status_message = ""
        network_status = 200

        # Send email here
        info = EmailSentToUsers.objects.create(
            email_type=email_type,
            sent_from_ip_address=client_address,
            email_sent_to=to_email,
            email_sent_from=from_email,
            subject=subject,
            message=message,
        )
        try:
            mail.send_simple_message(
                subject=info.subject,
                from_email=info.email_sent_from,
                to_email=info.email_sent_to,
                message=info.message,
            )
            status_message = "Email sent successfully"
            info.is_success = True
            info.save()
        except Exception as e:
            status_message = "Sorry unable to send email. Please try again later. Reason - {}".format(
                str(e)
            )
            failed = True
            network_status = 503
            info.is_success = True
            info.save()

        return Response(
            {
                "status": failed,
                "message": status_message,
                "detail": {
                    "id": info.id,
                    "email_type": info.email_type,
                    "sent_from_ip_address": info.client_address,
                    "email_sent_to": info.to_email,
                    "email_sent_from": info.from_email,
                    "subject": info.subject,
                    "message": info.message,
                    "sent_on": info.sent_on,
                    "is_success": info.is_success,
                },
            },
            status=network_status,
        )


class AllEmail(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EmailSentToUsersSerializer
    queryset = EmailSentToUsers.objects.all()
    filterset_fields = ["email_type", "email_sent_from", "email_sent_to", "is_success"]


class ListCreateUserLoginActivity(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserLoginActivitySerializer
    queryset = UserLoginActivity.objects.all().order_by("-timestamp")
    filterset_fields = [
        "user",
        "ip_address",
        "os_platform",
        "browser",
        "is_logged_from_mobile",
        "is_logged_from_web",
    ]


class UpdateUserLoginActivity(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserLoginActivitySerializer
    queryset = UserLoginActivity.objects.all().order_by("-timestamp")
    lookup_field = "id"

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ListCreateUserDeviceRegistration(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserDeviceRegistrationSerializer
    queryset = UserDeviceRegistration.objects.all().order_by("-timestamp")
    filterset_fields = [
        "user",
        "device_type",
        "operating_system",
        "browser",
        "ip_addresss",
        "lat",
        "lng",
        "device_language",
        "is_app",
        "is_browser",
    ]


class UpdateUserDeviceRegistration(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserDeviceRegistrationSerializer
    queryset = UserDeviceRegistration.objects.all().order_by("-timestamp")
    lookup_field = "id"

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ListAllNetworkOrders(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NetworkOrderSerializer
    queryset = NetworkOrder.objects.all().order_by("-timestamp")
    filterset_fields = [
        "network__user",
        "network__network_url",
        "network__network_type",
        "network__name",
        "network__landmark",
        "network__city",
        "network__state",
        "network__country",
        "network__pincode",
        "network__rating",
        "network__no_of_reviews",
        "network__registered_stores",
        "network__is_verified",
        "network__is_active",
        "network__is_spam",
        "network__is_premium",
        "order__id",
        "order__day_id",
        "order__billing_address",
        "order__shipping_address",
        "order__is_billing_shipping_same",
        "order__cart__user",
        "order__cart__count",
        "order__cart__sub_total",
        "order__cart__shipping",
        "order__cart__total",
        "order__cart__discount",
        "order__cart__is_active",
        "order__status",
        "order__shipping_total",
        "order__discount",
        "order__total",
        "order__tax",
        "order__active",
    ]


class UpdateNetworkOrder(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NetworkOrderSerializer
    queryset = NetworkOrder.objects.all()
    lookup_field = "id"

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class FileUploadView(APIView):
    parser_class = [FileUploadParser]
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        if "file" not in request.data:
            raise ParseError("FIle should be provided")
        file_obj = request.data["file"]
        filetype = request.data["filetype"]
        url = files.upload(file_obj, filetype)
        return Response(
            {
                "status": True,
                "message": "File Uploaded",
                "url": url,
            },
            status=201,
        )

    def get(self, request, format=None):
        return Response({"message": "Hello world"})


class FileView(APIView):
    parser_classes = [FileUploadParser]
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        if "file" not in request.data:
            raise ParseError("FIle should be provided")
        file_obj = request.data["file"]
        filetype = request.data["filetype"]
        url = upload.upload_file(file_obj, filetype)
        return Response(
            {
                "status": True,
                "message": "File Uploaded",
                "url": url,
            },
            status=201,
        )
