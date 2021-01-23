import json
from django.core import serializers as sj
from django.db.models import Q

from rest_framework import generics, permissions
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView, Response
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.exceptions import ParseError
from rest_framework.pagination import PageNumberPagination

from .models import *
from .serializers import *
from .permissions import *

from product_catalog.models import Product
from network.models import Network
from orders.models import Order
from product_catalog.serializers import ProductMiniSerializer
from network.serializers import ShowNetworkSerializer
from orders.serializers import ListOrderSerializer

from monorbit.utils import mail, upload, files


class ListCreateTipToGrow(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsAdmin]
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsAdmin]
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
    permission_classes = [permissions.IsAdminUser]
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
        "ip_address",
        "lat",
        "lng",
        "device_language",
        "is_app",
        "is_browser",
    ]


class UpdateUserDeviceRegistration(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated,UserDeviceOwner]
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
        "network",
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
        "network__is_basic",
        "network__is_economy",
        "network__is_elite",
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
    permission_classes = [permissions.IsAdminUser,NetworkOrderOwner]
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
        try:
            name = request.META["HTTP_NAME"]
        except:
            name = "hello.png"
        try:
            url, ext = files.upload(file_obj, filetype, name)
        except Exception as e:
            raise ValidationError(detail="Unable to upload file. Reason - {}".format(e), code=400)
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


class MultiFileUploadView(APIView):
    parser_class = [FileUploadParser]
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        if "file1" not in request.data:
            raise ParseError("Atleast one file should be provided")
        total_files = []
        total_files.append(request.data.get("file1", None))
        total_files.append(request.data.get("file2", None))
        total_files.append(request.data.get("file3", None))
        total_files.append(request.data.get("file4", None))
        total_files.append(request.data.get("file5", None))
        # no_of_images = request.data['no_of_images']
        names = request.data["names"]
        loaded_urls = []
        try:
            for i in total_files:
                if i is not None:
                    url, ext = files.upload(i, 'IMG', names[0])
                    loaded_urls.append(url)
        except Exception as e:
            raise ValidationError(detail="Unable to upload file. Reason - {}".format(e), code=400)
        return Response(
            {
                "status": True,
                "message": "Files Uploaded",
                "urls": loaded_urls,
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


class ProductsSearch(APIView):
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberPagination

    def get(self, request, format=None):
        query = request.query_params.get('query', None)
        network = request.query_params.get('network', None)

        if network is None:
            raise ValidationError(detail="You have to provide network in order to search", code=400)
        else:
            products = Product.objects.filter(Q(name__icontains=query) | Q(brand_name__icontains=query) | Q(short_description__icontains=query), network=network)
            # result_page =  self.paginate_queryset(products, request)
            # serializer = ProductMiniSerializer(result_page, many=True, context={'request':request})

            page = self.paginate_queryset(products)
            if page is not None:
                serializer = ProductMiniSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data) 

    

class NetworkSearch(APIView):
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberPagination

    def get(self, request, format=None):
        query = request.query_params.get('query', None)
        network_type = request.query_params.get('type', 1)
        landmark =  request.query_params.get('landmark', None)
        city =  request.query_params.get('city', None)
        state =  request.query_params.get('state', None)
        pincode =  request.query_params.get('pincode', None)

        networks = Network.objects.filter(Q(name__icontains=query) & Q(landmark__icontains=landmark) & Q(city__icontains=city) & Q(state__icontains=state) & Q(pincode__icontains=pincode) & Q(network_type__id=network_type))
        # result_page =  self.paginate_queryset(products, request)
        # serializer = ProductMiniSerializer(result_page, many=True, context={'request':request})

        page = self.paginate_queryset(networks)
        if page is not None:
            serializer = ShowNetworkSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data) 

    

class OrderSearch(APIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    def get(self, request, format=None):
        query = request.query_params.get('query', None)

        orders = Order.objects.filter(Q(id__icontains=query) | Q(day_id__icontains=query))
        # result_page =  self.paginate_queryset(products, request)
        # serializer = ProductMiniSerializer(result_page, many=True, context={'request':request})

        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = ListOrderSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data) 
