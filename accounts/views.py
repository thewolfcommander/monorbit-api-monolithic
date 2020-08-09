from django.utils import timezone
from rest_framework import generics, permissions, authentication
from rest_framework.views import APIView, status, Response

from rest_framework_jwt.utils import jwt_encode_handler, jwt_payload_handler

from . import models as acc_models
from .permissions import IsOwner
from . import serializers as acc_serializers
from monorbit.utils import tools


class LoginView(APIView):
    """
    This login route will return useful user information only along with token
    """
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        serializer = acc_serializers.ObtainTokenSerializer(data=request.data)
        if serializer.is_valid():
            user_obj = acc_models.User.objects.get(mobile_number=serializer.validated_data['mobile_number'])

            if user_obj.is_active:
                token = jwt_encode_handler(jwt_payload_handler(user_obj))
                user_obj.is_logged_in = True
                user_obj.last_logged_in_time = timezone.now()
                user_obj.save()
                return Response(data={
                    'status': True,
                    'token': token, 
                    'user': {
                        'mobile_number': user_obj.mobile_number,
                        'full_name': user_obj.full_name,
                        'email': user_obj.email,
                        'hash_token': user_obj.hash_token,
                        'is_consumer': user_obj.is_consumer,
                        'is_creator': user_obj.is_creator,
                        'is_logged_in': user_obj.is_logged_in,
                        'is_working_profile': user_obj.is_working_profile,
                        'is_mobile_verified': user_obj.is_mobile_verified,
                        'is_email_verified': user_obj.is_email_verified,
                    },
                    'message': "User logged in Successfully"
                }, status=200)
            else:
                return Response(data={
                    'status': False,
                    'message': "Invalid User. Unable to Login"
                }, status=400)
        elif not serializer.is_valid():
            try:
                return Response(data={
                    'message': "{}".format(str(serializer.errors["non_field_errors"][0])),
                    'status': False
                }, status=400)
            except:
                return Response(data={
                    'message': "{} - Error".format(str(serializer.errors['mobile_number'][0])),
                    'status': False
                }, status=400)
        else:
            return Response(data={
                'message': "Some unknown Error occured. Please try again later.", 
                'status': False
            }, status=400)



class RegisterView(APIView):
    """
    This register route will return useful user information only along with token
    """
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = acc_serializers.UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            is_agreed_to_terms = serializer.validated_data['is_agreed_to_terms']
            password = serializer.validated_data['password']
            if is_agreed_to_terms:
                usr = serializer.save()
                otp_obj = acc_models.EmailVerifyOTP.objects.create(user=usr)
                usr.otp_sent += 1
                usr.set_password(password)
                usr.hash_token = tools.random_number_generator(111111111111, 99999999999)
                usr.save()
                data = {
                    'status': True,
                    "message": "OTP Sent to Mobile Number",
                    "otp": otp_obj.otp,
                    'mobile_number': serializer.validated_data['mobile_number'],
                }
                return Response(data=data, status=201)
            else:
                data = {
                    'status': False,
                    "message": "You have to accept the terms and conditions"
                }
                return Response(data=data, status=400)
        elif not serializer.is_valid():
            try:
                return Response(data={
                    'message': "{}".format(str(serializer.errors["non_field_errors"][0])),
                    'status': False
                }, status=400)
            except:
                return Response(data={
                    'message': "{} - Error".format(str(serializer.errors['mobile_number'][0])),
                    'status': False
                }, status=400)
        else:
            return Response(data={
                'message': "Some unknown Error occured. Please try again later.", 
                'status': False
            }, status=400)
        return Response(serializer.errors, status=400)


class VerifyOTPView(APIView):
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        mobile_number = request.data.get('mobile_number')
        otp = request.data.get('otp')
        if mobile_number is None:
            data = {
                'status': False,
                "message": "Invalid Mobile Number"
            }
            return Response(data, status=400)

        try:
            usr_obj = acc_models.User.objects.get(mobile_number=mobile_number)
            otp_obj = acc_models.EmailVerifyOTP.objects.filter(user=usr_obj)

            if usr_obj.is_mobile_verified:
                return Response(data={
                    'message': "Mobile number is already verified",
                    'status': True
                }, status=200)
            if otp_obj.exists():
                otp_obj = otp_obj.first()
                if otp_obj.expiry < timezone.now():
                    return Response(data={
                        'message': "Invalid OTP. OTP Expired",
                        'status': False
                    }, status=400)
                elif otp_obj.expiry >= timezone.now():
                    if otp_obj.otp == otp:
                        token = jwt_encode_handler(jwt_payload_handler(usr_obj))
                        usr_obj.is_logged_in = True
                        usr_obj.last_logged_in_time = timezone.now()
                        usr_obj.is_mobile_verified = True
                        usr_obj.save()
                        otp_obj.delete()
                        data = {
                            'status': True,
                            'message': "OTP successfully verified.",
                            'token': token,
                            'user': {
                                'mobile_number': usr_obj.mobile_number,
                                'full_name': usr_obj.full_name,
                                'email': usr_obj.email,
                                'hash_token': usr_obj.hash_token,
                                'is_consumer': usr_obj.is_consumer,
                                'is_logged_in': usr_obj.is_logged_in,
                                'is_creator': usr_obj.is_creator,
                                'is_working_profile': usr_obj.is_working_profile,
                                'is_mobile_verified': usr_obj.is_mobile_verified,
                                'is_email_verified': usr_obj.is_email_verified,
                            }
                        }
                        return Response(data=data, status=200)
                    else:
                        return Response(data={
                            'message': "Invalid OTP. May be a wrong otp",
                            'status': False
                        }, status=400)
                else:
                    return Response(data={
                        'message': "Invalid Request.",
                        'status': False
                    }, status=400)
            else:
                return Response(data={
                    'message': "Invalid OTP. May be a wrong otp",
                    'status': False
                }, status=400)
        except acc_models.User.DoesNotExist:
            return Response(data={
                'message': "Invalid Mobile Number",
                'status': False
            }, status=400)

        return Response(data={
            'message': "Something unusual happened. Please try again later.",
            'status': False
        }, status=400)

    
class ResendMobileVerifyOTPView(APIView):
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        mobile_number = request.data.get('mobile_number')
        if mobile_number is None:
            data = {
                'status': False,
                "message": "Invalid Mobile Number"
            }
            return Response(data, status=400)

        
        
        usr_obj = acc_models.User.objects.filter(mobile_number=mobile_number, is_active=True)
        if user.exists():
            user = usr_obj.first()
            if user.is_mobile_verified:
                data = {
                    'status': True,
                    "message": "User is Already Verified"
                }
                return Response(data, status=200)

            elif user.is_mobile_verified == False and user.otp_sent <= 3:
                otp = models.EmailVerifyOTP.objects.filter(user=user)
                if otp.exists():
                    otp.delete()
                otp = models.EmailVerifyOTP.objects.create(user=user)
                data = {
                    'status': True,
                    'otp': otp.otp,
                    'message': "OTP Sent successfully"
                }
                return Response(data, status=200)
                # subject = "No Reply | Encap OTP to verify email | Link will expire in 30 minutes"
                # from_email = "encapsummary@gmail.com"
                # to_email = user.email
                # message = """
                # Hi user,
                # Here's your otp to verify the email. Enter this otp to the application.
                # Warning: Do not share this with anyone
                # OTP - {}
                # The otp will expire in 30 minutes.
                # Regards, Encapsummary
                # """.format(otp.otp)
                # try:
                #     send_mail(
                #         subject,
                #         message,
                #         from_email,
                #         [to_email,]
                #     )
                #     user.otp_sent += 1
                #     user.save()
                #     data = {
                #         'status': True,
                #         'otp': otp.otp,
                #         'message': 'OTP Sent Successfully'
                #     }
                #     return Response(data, status=400)
                # except:
                #     otp.delete()
                #     data = {
                #         'status': False,
                #         'message': 'Can\'t send otp'
                #     }
                    # return Response(data, status=400)
            else:
                data = {
                    'status': False,
                    'message': 'You have requested maximum otp limit'
                }
                return Response(data, status=400)
        else:
            data = {
                'status': False,
                "message": "Invalid Mobile Number"
            }
            return Response(data, status=400)

        return Response(data={
            'message': "Something unusual happened. Please try again later.",
            'status': False
        }, status=400)


class GetUserInfo(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    serializer_class = acc_serializers.UserInfoSerializer
    queryset = acc_models.User.objects.all()
    lookup_field = 'mobile_number'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class RefreshToken(APIView):
    permission_classes = (permissions.IsAuthenticated)
    
    def get(self, request, format=None):
        try:
            user = request.user
            token = jwt_encode_handler(jwt_payload_handler(user))
            return Response({
                'status': True,
                'message': "Token refreshed successfully",
                'token': token
            }, status=200)
        except Exception as exc:
            return Response(str(exc), status=400)

    
class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated)
    
    def get(self, request, format=None):
        try:
            user = request.user
            user.is_logged_in = False
            user.save()
            return Response({
                'status': True,
                'message': "Successfully Logged Out",
            }, status=200)
        except Exception as exc:
            return Response({
                "message": str(exc),
                "status": False
            }, status=400)

        
class DeleteAccount(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    serializer_class = acc_serializers.UserDeleteSerializer
    queryset = acc_models.User.objects.all()
    lookup_field = 'mobile_number'
