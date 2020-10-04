from django.utils import timezone
from django.contrib.auth.hashers import check_password
from rest_framework import generics, permissions, authentication
from rest_framework.views import APIView, status, Response

from rest_framework_jwt.utils import jwt_encode_handler, jwt_payload_handler

from . import models as acc_models
from .permissions import IsOwner
from . import serializers as acc_serializers
from monorbit.utils import tools, sms, data

import logging
logger = logging.getLogger(__name__)

def expiration_delta():
    return timezone.now() + timezone.timedelta(minutes=10)


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
                        'followed_networks': user_obj.followed_networks,
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
                if "mobile_number" in serializer.errors:
                    return Response(data={
                        'message': "{} - Error".format(str(serializer.errors['mobile_number'][0])),
                        'status': False
                    }, status=400)
                else:
                    return Response(data={
                        'message': "{} - Error".format(str(serializer.errors['password'][0])),
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
                string = "MONO{}".format(str(serializer.validated_data['mobile_number']))
                usr.hash_token = tools.label_gen(string)
                usr.save()
                mobile = "+91{}".format(str(serializer.validated_data['mobile_number']))
#                 sms.verify_mobile(mobile_number=mobile, otp=otp_obj.otp)
                data = {
                    'status': True,
                    "message": "OTP Sent to Mobile Number",
                    "otp": otp_obj.otp,
                    'mobile_number': usr.mobile_number,
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
                for i in serializer.errors:
                    return Response(data={
                        'message': "{} - Error in {}".format(str(serializer.errors[i][0]), str(i)),
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
                if timezone.now() > (otp_obj.created + timezone.timedelta(minutes=10)):
                    return Response(data={
                        'message': "Invalid OTP. OTP Expired",
                        'status': False
                    }, status=400)
                elif timezone.now() <= (otp_obj.created + timezone.timedelta(minutes=10)):
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
                                'followed_networks': usr_obj.followed_networks,
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
        if usr_obj.exists():
            user = usr_obj.first()
            if user.is_mobile_verified:
                data = {
                    'status': True,
                    "message": "User is Already Verified"
                }
                return Response(data, status=200)

            elif user.is_mobile_verified == False and user.otp_sent <= 3:
                otp = acc_models.EmailVerifyOTP.objects.filter(user=user)
                if otp.exists():
                    otp.delete()
                otp = acc_models.EmailVerifyOTP.objects.create(user=user)
#                 sms.verify_mobile(mobile_number="+91{}".format(str(mobile_number)), otp=otp.otp)
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


 
class ForgotPasswordView(APIView):
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
        if usr_obj.exists():
            user = usr_obj.first()

            if user.password_otp_sent <= 3:
                otp = acc_models.PasswordResetToken.objects.filter(user=user)
                if otp.exists():
                    otp.delete()
                otp = acc_models.PasswordResetToken.objects.create(user=user)
                user.password_otp_sent += 1
                user.save()
#                 sms.verify_mobile(mobile_number="+91{}".format(str(mobile_number)), otp=otp.token)
                data = {
                    'status': True,
                    'otp': otp.token,
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
                "message": "No User related with this mobile number."
            }
            return Response(data, status=400)

        return Response(data={
            'message': "Something unusual happened. Please try again later.",
            'status': False
        }, status=400)

    
class ResetPasswordView(APIView):
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        mobile_number = request.data.get('mobile_number')
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')
        if mobile_number is None:
            data = {
                'status': False,
                "message": "Mobile Number should be provided"
            }
            return Response(data, status=400)
        usr_obj = acc_models.User.objects.filter(mobile_number=mobile_number, is_active=True)
        if usr_obj.exists():
            user = usr_obj.first()
            otp_obj = acc_models.PasswordResetToken.objects.filter(user=user)
            if otp_obj.exists():
                if timezone.now() > (otp_obj.first().created + timezone.timedelta(minutes=10)):
                    return Response(data={
                        'message': "Invalid OTP. OTP Expired",
                        'status': False
                    }, status=400)
                elif timezone.now() <= (otp_obj.first().created + timezone.timedelta(minutes=10)):
                    if otp_obj.first().token == otp:
                        user.set_password(new_password)
                        user.save()
                        otp_obj.delete()
                        data = {
                            'status': True,
                            'message': "Password reset successfull"
                        }
                        return Response(data, status=200)
                    else:
                        data = {
                            'status': False,
                            'message': "Invalid OTP"
                        }
                        return Response(data, status=400)
                else:
                    data = {
                        'status': False,
                        'message': "Invalid OTP"
                    }
                    return Response(data, status=400)
            else:
                data = {
                    'status': False,
                    'message': "Invalid OTP"
                }
                return Response(data, status=400)
        else:
            data = {
                'status': False,
                "message": "No User related with this mobile number."
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
    permission_classes = (permissions.IsAuthenticated,)
    
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
    permission_classes = (permissions.IsAuthenticated,)
    
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


class SudoModeAuthenticationView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request, format=None):
        user = request.user
        password = request.data.get('password', None)

        if password is None:
            return Response({
                "status": False,
                "message": "You have to provide password"
            }, status=400)

        if check_password(password, user.password):
            return Response({
                "status": True,
                "message": "You have permission to do the stuff"
            }, status=200)
        else:
            return Response({
                "status": False,
                "message": "Your access is denied. Please check the password"
            }, status=403)

        
class UserLanguage(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user

        try:
            instance = acc_models.UserLocalization.objects.create(user=user)
            return Response({
                'status': True,
                'user': user.mobile_number,
                'communication_language_code': instance.communication_language_code,
                'interface_language_code': instance.interface_language_code,
            }, status=200)
        except acc_models.UserLocalization.DoesNotExist:
            return Response({
                'status': False,
                'message': 'Localization not found for current user.',
            }, status=400)


    def post(self, request, format=None):
        user = request.user
        communication_language_code = request.data.get('communication_language_code', None)
        interface_language_code = request.data.get('interface_language_code', None)

        if communication_language_code is None:
            return Response({
                'status': False,
                'message': 'No communication language provided. Please try again by providing a valid language.'
            }, status=400)

        if interface_language_code is None:
            return Response({
                'status': False,
                'message': 'No interface language provided. Please try again by providing a valid language.'
            }, status = 400)

        try:
            print(acc_models.UserLocalization.objects.filter(user=user))
            instance = acc_models.UserLocalization.objects.get(user=user)
            instance.communication_language_code = communication_language_code
            instance.interface_language_code = interface_language_code
            instance.save()
            return Response({
                'status': True,
                'message': 'Language set successful.',
                'communication_language_code': instance.communication_language_code,
                'interface_language_code': instance.interface_language_code
            }, status=200)
        except acc_models.UserLocalization.DoesNotExist:
            instance = acc_models.UserLocalization.objects.create(
                user=user,
                communication_language_code=communication_language_code,
                interface_language_code=interface_language_code,
            )

            return Response({
                'status': True,
                'message': 'Language set successful.',
                'communication_language_code': instance.communication_language_code,
                'interface_language_code': instance.interface_language_code
            }, status=201)
