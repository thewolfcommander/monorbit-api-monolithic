from rest_framework import generics, permissions
from rest_framework.views import APIView, Response

from .models import *
from .serializers import *

from monorbit.utils import mail


class ListCreateTipToGrow(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TipToGrowSerializer
    queryset = TipToGrow.objects.all()
    filterset_fields = [
        'upvotes',
        'downvotes',
        'active'
    ]


class UpdateTipToGrow(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TipToGrowSerializer
    queryset = TipToGrow.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    
class SendEmail(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        from_email = request.data.get('from_email', 'support@monorbit.com')
        email_type = request.data.get('email_type')
        to_email = request.data.get('to_email')
        subject = request.data.get('subject')
        message = request.data.get('message')
        client_address = request.META['HTTP_X_FORWARDED_FOR']
        failed = False
        status_message = ''
        network_status = 200

        # Send email here
        info = EmailSentToUsers.objects.create(
            email_type=email_type,
            sent_from_ip_address = client_address,
            email_sent_to=to_email,
            email_sent_from=from_email,
            subject=subject,
            message = message
        )
        try:
            mail.send_simple_message(
                subject=info.subject,
                from_email=info.email_sent_from,
                to_email=info.email_sent_to,
                message=info.message
            )
            status_message = "Email sent successfully"
            info.is_success = True
            info.save()
        except Exception as e:
            status_message = "Sorry unable to send email. Please try again later. Reason - {}".format(str(e))
            failed = True
            network_status = 503
            info.is_success = True
            info.save()

        
        return Response({
            'status': failed,
            'message': status_message,
            'detail': {
                'id': info.id,
                'email_type':info.email_type,
                'sent_from_ip_address' : info.client_address,
                'email_sent_to':info.to_email,
                'email_sent_from':info.from_email,
                'subject':info.subject,
                'message' : info.message,
                'sent_on': info.sent_on,
                'is_success': info.is_success,
            }
        }, status=network_status)


class AllEmail(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EmailSentToUsersSerializer
    queryset = EmailSentToUsers.objects.all()
    filterset_fields = [
        'email_type',
        'email_sent_from',
        'email_sent_to',
        'is_success'
    ]


class ListCreateUserLoginActivity(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserLoginActivitySerializer
    queryset = UserLoginActivity.objects.all().order_by('-timestamp')
    filterset_fields = [
        'user',
        'ip_address',
        'os_platform',
        'browser',
        'is_logged_from_mobile',
        'is_logged_from_web'
    ]


class UpdateUserLoginActivity(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserLoginActivitySerializer
    queryset = UserLoginActivity.objects.all().order_by('-timestamp')
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    

class ListCreateUserDeviceRegistration(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserDeviceRegistrationSerializer
    queryset = UserDeviceRegistration.objects.all().order_by('-timestamp')
    filterset_fields = [
        'user',
        'device_type',
        'operating_system',
        'browser',
        'ip_addresss',
        'lat',
        'lng',
        'device_language',
        'is_app',
        'is_browser',
    ]


class UpdateUserDeviceRegistration(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserDeviceRegistrationSerializer
    queryset = UserDeviceRegistration.objects.all().order_by('-timestamp')
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)