import re

from django.utils import timezone
from django.contrib.auth.hashers import check_password
from rest_framework import generics, permissions, authentication
from rest_framework.views import APIView, status, Response
from rest_framework.serializers import ValidationError

from rest_framework_jwt.utils import jwt_encode_handler, jwt_payload_handler

from . import models as acc_models
from .permissions import IsOwner
from . import serializers as acc_serializers
from monorbit.utils import tools, sms, data, mail

import logging

logger = logging.getLogger(__name__)


def expiration_delta():
    return timezone.now() + timezone.timedelta(minutes=10)


class UserListView(generics.ListAPIView):
    """
    This route will list all the users registered on monorbit
    """
    authentication_classes = ()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = acc_serializers.UserInfoSerializer
    queryset = acc_models.User.objects.all()

    filterset_fields = [
        'mobile_number',
        'id',
        'hash_token',
        'country_code',
        'gender',
        'registration_reference',
        'city',
        'pincode',
        'network_created',
        'otp_sent',
        'password_otp_sent',
        'order_count',
        'is_consumer',
        'followed_networks',
        'is_creator',
        'is_working_profile',
        'is_active',
        'is_agreed_to_terms',
        'is_admin',
        'is_mobile_verified',
        'is_email_verified',
        'is_logged_in',
        'is_archived',
    ]


class AdminLoginView(APIView):
    """
    This login route will return useful user information only along with token only for admin users
    """

    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        # accessing serializer
        serializer = acc_serializers.ObtainTokenSerializer(data=request.data)
        if serializer.is_valid():
            user_obj = acc_models.User.objects.get(
                mobile_number=serializer.validated_data["mobile_number"]
            )

            if user_obj.is_active and user_obj.is_admin:
                # getting token from jwt
                token = jwt_encode_handler(jwt_payload_handler(user_obj))
                user_obj.is_logged_in = True
                user_obj.last_logged_in_time = timezone.now()
                user_obj.save()
                return Response(
                    data={
                        "status": True,
                        "token": token,
                        "user": {
                            "id": user_obj.id,
                            "mobile_number": user_obj.mobile_number,
                            "full_name": user_obj.full_name,
                            "email": user_obj.email,
                            "hash_token": user_obj.hash_token,
                            "is_consumer": user_obj.is_consumer,
                            "is_creator": user_obj.is_creator,
                            "followed_networks": user_obj.followed_networks,
                            "is_logged_in": user_obj.is_logged_in,
                            "is_admin": user_obj.is_admin,
                            "is_working_profile": user_obj.is_working_profile,
                            "is_mobile_verified": user_obj.is_mobile_verified,
                            "is_email_verified": user_obj.is_email_verified,
                        },
                        "message": "User logged in Successfully",
                    },
                    status=200,
                )
            else:
                raise ValidationError(detail="invalid User. Unable to Login", code=400)
        elif not serializer.is_valid():
            try:
                raise ValidationError(detail= "{}".format(
                            str(serializer.errors["non_field_errors"][0])
                        ), code=400)
            except:
                if "mobile_number" in serializer.errors:
                    raise ValidationError(detail="{} - Error".format(
                                str(serializer.errors["mobile_number"][0])
                            ), code=400)
                else:
                    raise ValidationError(detail="{} - Error".format(
                                str(serializer.errors["password"][0])
                            ), code=400)
        else:
            raise ValidationError(detail="Some unknown Error occured. Please try again later.", code=400)


class LoginView(APIView):
    """
    This login route will return useful user information only along with token
    """

    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = acc_serializers.ObtainTokenSerializer(data=request.data)
        if serializer.is_valid():
            # Getting the user object for the mobile number input from user
            user_obj = acc_models.User.objects.get(
                mobile_number=serializer.validated_data["mobile_number"]
            )

            if user_obj.is_active:
                # Checking if user's mobile number is verified or not. If mobile number is verified then logged in, otherwise send otp.(for following if block)
                if user_obj.is_mobile_verified:
                    token = jwt_encode_handler(jwt_payload_handler(user_obj))
                    user_obj.is_logged_in = True
                    user_obj.last_logged_in_time = timezone.now()
                    user_obj.save()
                    return Response(
                        data={
                            "status": True,
                            "token": token,
                            "user": {
                                "id": user_obj.id,
                                "mobile_number": user_obj.mobile_number,
                                "full_name": user_obj.full_name,
                                "email": user_obj.email,
                                "hash_token": user_obj.hash_token,
                                "is_consumer": user_obj.is_consumer,
                                "is_creator": user_obj.is_creator,
                                "followed_networks": user_obj.followed_networks,
                                "is_logged_in": user_obj.is_logged_in,
                                "is_working_profile": user_obj.is_working_profile,
                                "is_mobile_verified": user_obj.is_mobile_verified,
                                "is_email_verified": user_obj.is_email_verified,
                            },
                            "message": "User logged in Successfully",
                        },
                        status=200,
                    )
                else:
                    # Creating OTP object
                    otp_obj = acc_models.EmailVerifyOTP.objects.create(user=user_obj)
                    # updating otp_sent count so that we can send maximum 3 otp.
                    user_obj.otp_sent += 1
                    user_obj.save()
                    # sending otp to mobile number
                    mobile = "+91{}".format(str(serializer.validated_data["mobile_number"]))
                    sms.verify_mobile(mobile_number=mobile, otp=otp_obj.otp)
                    data = {
                        "status": True,
                        "message": "OTP Sent to Mobile Number",
                        "mobile_number": user_obj.mobile_number,
                    }
                    return Response(data=data, status=201)
            else:
                raise ValidationError(detail="Invalid User. Unable to Login", code=400)
                
        elif not serializer.is_valid():
            try:
                raise ValidationError(detail="{}".format(
                            str(serializer.errors["non_field_errors"][0])
                        ), code=400)
            except:
                for i in serializer.errors:
                    raise ValidationError(detail="{}".format(
                                str(serializer.errors[i][0]), str(i)
                            ), code=400)      
        else:
            raise ValidationError(detail="Some unknown Error occured. Please try again later.", code=400)


class RegisterView(APIView):
    """
    This register route will return useful user information only along with token
    """

    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = acc_serializers.UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            is_agreed_to_terms = serializer.validated_data["is_agreed_to_terms"]
            password = serializer.validated_data["password"]
            # Checking that User is agreed to terms and conditions or not. If is_agreed_to_terms is True then proceed, otherwise raise error. (for following If block) 
            if is_agreed_to_terms:
                usr = serializer.save()
                # Creating OTP object
                otp_obj = acc_models.EmailVerifyOTP.objects.create(user=usr)
                # updating otp_sent count so that we can send maximum 3 otp.
                usr.otp_sent += 1
                usr.set_password(password)
                string = "MONO{}".format(
                    str(serializer.validated_data["mobile_number"])
                )
                # Generating unique hash token for each user
                usr.hash_token = tools.label_gen(string)
                usr.save()
                mobile = "+91{}".format(str(serializer.validated_data["mobile_number"]))
                # sending mobile otp to user
                sms.verify_mobile(mobile_number=mobile, otp=otp_obj.otp)
                data = {
                    "status": True,
                    "message": "OTP Sent to Mobile Number",
                    "mobile_number": usr.mobile_number,
                }
                return Response(data=data, status=201)
            else:
                raise ValidationError(detail="You have to accept the terms and conditions", code=400)
                
        elif not serializer.is_valid():
            try:
                raise ValidationError(detail="{}".format(
                            str(serializer.errors["non_field_errors"][0])
                        ), code=400)
            except:
                for i in serializer.errors:
                    raise ValidationError(detail="{} - Error in {}".format(
                                str(serializer.errors[i][0]), str(i)
                            ), code=400)
        else:
            raise ValidationError(detail="Some unknown Error occured. Please try again later.", code=400)
            
        raise ValidationError(detail=serializer.errors, code=400)


class VerifyOTPView(APIView):
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        mobile_number = request.data.get("mobile_number")
        otp = request.data.get("otp")
        if mobile_number is None:
            data = {"status": False, "message": "Invalid Mobile Number"}
            return Response(data, status=400)

        try:
            # Fetching user obj from user model based on mobile number.
            usr_obj = acc_models.User.objects.get(mobile_number=mobile_number)
            # using above user obj, fetching otp obj.
            otp_obj = acc_models.EmailVerifyOTP.objects.filter(user=usr_obj)
            
            # Checking if user's mobile number is verified or not. If verified then send response that "Mobile number is already verified".
            if usr_obj.is_mobile_verified:
                return Response(
                    data={
                        "message": "Mobile number is already verified",
                        "status": True,
                    },
                    status=200,
                )
            # If otp_obj exist then fetch the first object, compare the current timezone with otp_obj timezone(when object created) + 10 minutes.            
            if otp_obj.exists():
                otp_obj = otp_obj.first()
                # if current timezone is greater than otp_obj timezone+10 minutes then raise error OTP expired.
                if timezone.now() > (otp_obj.created + timezone.timedelta(minutes=10)):
                    raise ValidationError(detail="Invalid OTP. OTP Expired", code=400)

                # Otherwise proceed.  
                elif timezone.now() <= (
                    otp_obj.created + timezone.timedelta(minutes=10)
                ):
                    # check request data OTP is equal to otp_obj's otp. If True then rewrite usr_object. After that delete otp_obj.
                    if otp_obj.otp == otp:
                        token = jwt_encode_handler(jwt_payload_handler(usr_obj))
                        usr_obj.is_logged_in = True
                        usr_obj.last_logged_in_time = timezone.now()
                        usr_obj.is_mobile_verified = True
                        usr_obj.save()
                        otp_obj.delete()
                        data = {
                            "status": True,
                            "message": "OTP successfully verified.",
                            "token": token,
                            "user": {
                                "id": usr_obj.id,
                                "mobile_number": usr_obj.mobile_number,
                                "full_name": usr_obj.full_name,
                                "email": usr_obj.email,
                                "hash_token": usr_obj.hash_token,
                                "followed_networks": usr_obj.followed_networks,
                                "is_consumer": usr_obj.is_consumer,
                                "is_logged_in": usr_obj.is_logged_in,
                                "is_creator": usr_obj.is_creator,
                                "is_working_profile": usr_obj.is_working_profile,
                                "is_mobile_verified": usr_obj.is_mobile_verified,
                                "is_email_verified": usr_obj.is_email_verified,
                            },
                        }
                        return Response(data=data, status=200)
                    else:
                        raise ValidationError(detail="Invalid OTP. May be a wrong otp", code=400)       
                else:
                    raise ValidationError(detail="Invalid Request.", code=400)
            else:
                raise ValidationError(detail="Invalid OTP. May be a wrong otp", code=400)
                
        except acc_models.User.DoesNotExist:
            raise ValidationError(detail="Invalid Mobile Number", code=400)

        raise ValidationError(detail="Something unusual happened. Please try again later.", code=400)

# Resending Mobile Otp
class ResendMobileVerifyOTPView(APIView):
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        mobile_number = request.data.get("mobile_number")
        if mobile_number is None:
            data = {"status": False, "message": "Invalid Mobile Number"}
            return Response(data, status=400)

        # Fetching user obj from user model based on mobile number and is_active.
        usr_obj = acc_models.User.objects.filter(
            mobile_number=mobile_number, is_active=True
        )
        # Checking user exist or not. If user exist then proceed.
        if usr_obj.exists():
            user = usr_obj.first()
            # checking user mobile number is verfied or not. If True then send message "User is Already Verified".
            if user.is_mobile_verified:
                data = {"status": True, "message": "User is Already Verified"}
                return Response(data, status=200)

            # if user mobile number is not verified and otp_send count is less than or equal to 3, then proceed.
            elif user.is_mobile_verified == False and user.otp_sent <= 3:
                # check if otp object is already exist for request user. if exist then first delete it.
                otp = acc_models.EmailVerifyOTP.objects.filter(user=user)
                if otp.exists():
                    otp.delete()
                # create new otp object for request user.
                otp = acc_models.EmailVerifyOTP.objects.create(user=user)
                # send OTP to mobile number
                sms.verify_mobile(mobile_number="+91{}".format(str(mobile_number)), otp=otp.otp)
                data = {
                    "status": True,
                    "message": "OTP Sent successfully",
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
                raise ValidationError(detail="You have requested maximum otp limit", code=400)        
        else:
            raise ValidationError(detail="Invalid Mobile Number", code=400)
        
        raise ValidationError(detail="Something unusual happened. Please try again later.", code=400)


class SendResetPasswordOTP(APIView):
    """
    This API will send the OTP on the user's mobile for password reset request only if the user found for the Monorbit
    """
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        """
        Method for handling post request on the API
        """
        mobile_number = request.data.get("mobile_number")
        if mobile_number is None:
            raise ValidationError(detail="Invalid Mobile Number", code=400)

        usr_obj = acc_models.User.objects.filter(
            mobile_number=mobile_number, is_active=True
        )

        if usr_obj.exists():
            user = usr_obj.first()    # Getting the very first instance of the user

            # check if password_otp_sent (to user) is less than or equal. If True then proceed.
            if user.password_otp_sent <= 3:
                # Check if the password OTP Object is already exist for request user. If exists then extend it's time and send it.
                otp = acc_models.PasswordResetToken.objects.filter(user=user)
                if otp.exists():
                    otp_obj = otp.first()
                    if timezone.now() > (otp_obj.created + timezone.timedelta(minutes=10)):
                        otp.delete()
                        # create new password otp object for request user.
                        otp_obj = acc_models.PasswordResetToken.objects.create(user=user)
                        # send otp to user mobile number.
                        sms.reset_password(mobile_number="+91{}".format(str(mobile_number)), otp=otp_obj.token)
                        # update password_otp_sent by +1.
                        user.password_otp_sent += 1
                        user.save()
                        try:
                            # send otp to user mail if email exist otherwise pass.
                            mail.send_reset_password_otp(user.email, otp_obj.token)
                        except:
                            pass
                        data = {
                            "status": True,
                            "message": "OTP Sent successfully",
                        }
                        return Response(data, status=200)
                    else:
                        # send otp to user mobile number.
                        sms.reset_password(mobile_number="+91{}".format(str(mobile_number)), otp=otp_obj.token)
                        # update password_otp_sent by +1.
                        user.password_otp_sent += 1
                        user.save()
                        try:
                            # send otp to user mail if email exist otherwise pass.
                            mail.send_reset_password_otp(user.email, otp_obj.token)
                        except:
                            pass
                        data = {
                            "status": True,
                            "message": "OTP Sent successfully",
                        }
                        return Response(data, status=200)
                else:
                    # create new password otp object for request user.
                    otp = acc_models.PasswordResetToken.objects.create(user=user)
                    # send otp to user mobile number.
                    sms.reset_password(mobile_number="+91{}".format(str(mobile_number)), otp=otp.token)
                    # update password_otp_sent by +1.
                    user.password_otp_sent += 1
                    user.save()
                    try:
                        # send otp to user mail if email exist otherwise pass.
                        mail.send_reset_password_otp(user.email, otp.token)
                    except:
                        pass
                    data = {
                        "status": True,
                        "message": "OTP Sent successfully",
                    }
                    return Response(data, status=200)
            else:
                raise ValidationError(detail="You have requested maximum number of OTP", code=400)
        else:
            raise ValidationError(detail="Invalid User.", code=404)        


class ResetPasswordVerifyOTPView(APIView):
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        # Get mobile_number, otp and new_password to reset password.
        mobile_number = request.data.get("mobile_number")
        otp = request.data.get("otp")
        if mobile_number is None:
            raise ValidationError(detail="Mobile Number should be provided", code=400)

        if otp is None:
            raise ValidationError(detail="OTP should be provided", code=400)
        # Fetching user obj from user model based on mobile number and is_active.
        usr_obj = acc_models.User.objects.filter(
            mobile_number=mobile_number, is_active=True
        )
        if usr_obj.exists():
            user = usr_obj.first()
            # Fetch password otp object based on above user.
            otp_obj = acc_models.PasswordResetToken.objects.filter(user=user)
            if otp_obj.exists():
                # if current timezone is greater than otp_obj timezone+10 minutes then raise error OTP expired.
                if timezone.now() > (
                    otp_obj.first().created + timezone.timedelta(minutes=10)
                ):
                    raise ValidationError(detail="Invalid OTP. OTP Expired", code=400)
                # Otherwise proceed
                elif timezone.now() <= (
                    otp_obj.first().created + timezone.timedelta(minutes=10)
                ):
                    # check otp_obj's token is equal to requested otp.if True, then reset the password, password_otp_sent count will 0 and delete otp_obj.
                    if otp_obj.first().token == otp:
                        data = {"status": True, "message": "OTP Verified Successfully", "user": user.id}
                        return Response(data, status=200)
                    else:
                        raise ValidationError(detail="Invalid OTP. 1", code=400)
                else:
                    raise ValidationError(detail="Invalid OTP. 2", code=400)
            else:
                raise ValidationError(detail="Invalid OTP. 3", code=400)
        else:
            raise ValidationError(detail="No User related with this mobile number.", code=400)


class ResetPasswordView(APIView):
    """
    This API will reset the user password
    """
    permission_classes = [permissions.AllowAny,]

    def post(self, request, format=None):
        user = request.data.get('user')
        new_password = request.data.get('new_password')

        if user is None:
            raise ValidationError(detail="Invalid User", code=400)

        if new_password is None:
            raise ValidationError(detail="New Password not provided. Please try again by providing the new password")


        try:
            user_obj = acc_models.User.objects.get(id=user)
            user_obj.set_password(new_password)
            user_obj.password_otp_sent = 0
            user_obj.save()

            return Response(data={
                'status': True,
                'message': "Password Changed Successfully. You can login now."
            }, status=200)
        except acc_models.User.DoesNotExist:
            raise ValidationError(detail="Invalid User. User not found", code=400)

# Getting user info by mobile number.
class GetUserInfo(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    serializer_class = acc_serializers.UserInfoSerializer
    queryset = acc_models.User.objects.all()
    lookup_field = "mobile_number"

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

# Refresh JWT token
class RefreshToken(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        try:
            user = request.user
            token = jwt_encode_handler(jwt_payload_handler(user))
            return Response(
                {
                    "status": True,
                    "message": "Token refreshed successfully",
                    "token": token,
                },
                status=200,
            )
        except Exception as exc:
            raise ValidationError(detail=str(exc), code=400)

# User Logout
class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        try:
            user = request.user
            user.is_logged_in = False
            user.save()
            return Response(
                {
                    "status": True,
                    "message": "Successfully Logged Out",
                },
                status=200,
            )
        except Exception as exc:
            raise ValidationError(detail=str(exc), code=400)

# Deleting user account (is_active=False)
class DeleteAccount(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    serializer_class = acc_serializers.UserDeleteSerializer
    queryset = acc_models.User.objects.all()
    lookup_field = "mobile_number"

# For advanced edit of user's info. User have to enter their password.
class SudoModeAuthenticationView(APIView):
    permission_classes = (permissions.IsAuthenticated,IsOwner)

    def post(self, request, format=None):
        user = request.user
        password = request.data.get("password", None)

        if password is None:
            raise ValidationError(detail="You have to provide password", code=400)
        
        # check the enter request password is eqaul to save password.
        if check_password(password, user.password):
            return Response(
                {"status": True, "message": "You have permission to do the stuff"},
                status=200,
            )
        else:
            raise ValidationError(detail="Your access is denied. Please check the password", code=403)

# Get and set user language
class UserLanguage(APIView):
    permission_classes = (permissions.IsAuthenticated,IsOwner)

    def get(self, request):
        user = request.user

        try:
            # creating user localization with default communication_language_code is "en" and communication_language_code is "en".
            instance = acc_models.UserLocalization.objects.create(user=user)
            return Response(
                {
                    "status": True,
                    "user": user.mobile_number,
                    "communication_language_code": instance.communication_language_code,
                    "interface_language_code": instance.interface_language_code,
                },
                status=200,
            )
        except acc_models.UserLocalization.DoesNotExist:
            raise ValidationError(detail="Localization not found for current user.", code=400)

    def post(self, request, format=None):
        user = request.user
        communication_language_code = request.data.get(
            "communication_language_code", None
        )
        interface_language_code = request.data.get("interface_language_code", None)

        if communication_language_code is None:
            raise ValidationError(detail="No communication language provided. Please try again by providing a valid language.", code=400)

        if interface_language_code is None:
            raise ValidationError(detail="No interface language provided. Please try again by providing a valid language.", code=400)

        try:
            # Fetch user's current language code.
            instance = acc_models.UserLocalization.objects.get(user=user)
            # overwrite with request communication_language_code and interface_language_code
            instance.communication_language_code = communication_language_code
            instance.interface_language_code = interface_language_code
            instance.save()
            return Response(
                {
                    "status": True,
                    "message": "Language set successful.",
                    "communication_language_code": instance.communication_language_code,
                    "interface_language_code": instance.interface_language_code,
                },
                status=200,
            )
        except acc_models.UserLocalization.DoesNotExist:
            # if current user have not set communication_language_code and interface_language_code, then create object.
            instance = acc_models.UserLocalization.objects.create(
                user=user,
                communication_language_code=communication_language_code,
                interface_language_code=interface_language_code,
            )

            return Response(
                {
                    "status": True,
                    "message": "Language set successful.",
                    "communication_language_code": instance.communication_language_code,
                    "interface_language_code": instance.interface_language_code,
                },
                status=201,
            )


class EmailVerificationEnter(APIView):
    permission_classes = [permissions.IsAuthenticated,IsOwner]

    def post(self, request, format=None):
        # Get email from request
        email = request.data.get("email", None)
        # Email verication regular expression
        regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        if email is None:
            raise ValidationError(detail="Please provide an email address to continue", code=400)
        
        # check request email is pass regex. If True, then proceed
        if re.search(regex, email):
            user = request.user
            # Check if email is verified or not. If already verified then return "Your email has been already verified. keep it up on board."
            if user.is_email_verified:
                return Response(
                    {
                        "status": True,
                        "message": "Your email has been already verified. keep it up on board.",
                    }
                )
            # check request email is current user's email. If True then proceed.
            if user.email == email:
                try:
                    # check otp object is already exist for current user.
                    otp = acc_models.EmailVerifyOTP.objects.get(user=user)
                    # delete already exist otp object.
                    otp.delete()
                    # create new otp object.
                    otp = acc_models.EmailVerifyOTP.objects.create(user=user)
                except acc_models.EmailVerifyOTP.DoesNotExist:
                    # check otp object is not already exist for current user, then create otp object
                    otp = acc_models.EmailVerifyOTP.objects.create(user=user)
                try:
                    # send otp to user's email
                    mail.send_otp_email_verification(user.email, otp.otp)
                    return Response(
                        {
                            "status": True,
                            "message": "An email with otp sent successfully to "
                            + str(user.email),
                        },
                        status=200,
                    )
                except:
                    raise ValidationError(detail="Sorry cannot send email at the moment. Please try again later.", code=500)
            else:
                raise ValidationError(detail="Unauthorized Request. Email address you entered is not accessible to your account.", code=403)
        else:
            raise ValidationError(detail="Please enter a valid email address.", code=400)


class VerifyEmailOTP(APIView):
    permission_classes = [permissions.IsAuthenticated,IsOwner]

    def post(self, request, format=None):
        # Get email from request
        email = request.data.get("email", None)
        # Get otp from request
        otp = request.data.get("otp", None)
        # Email verication regular expression
        regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        if email is None:
            raise ValidationError(detail="Please provide an email address to continue", code=400)
        if otp is None:
            raise ValidationError(detail="Please provide otp sent on your email address to continue.", code=400)
        
        # check request email is pass regex. If True, then proceed
        if re.search(regex, email):
            user = request.user
            # Check if email is verified or not. If already verified then return "Your email has been already verified. keep it up on board."
            if user.is_email_verified:
                return Response(
                    {
                        "status": True,
                        "message": "Your email has been already verified. keep it up on board.",
                    }
                )
            # check request email is current user's email. If True then proceed.
            if user.email == email:
                try:
                    # check otp object is already exist for current user.
                    otp_obj = acc_models.EmailVerifyOTP.objects.get(user=user)
                    # compare request otp with otp_obj's otp. If True then proceed.
                    if otp_obj.otp == otp:
                        if otp_obj.created >= timezone.now():
                            otp_obj.delete()
                            raise ValidationError(detail="Invalid OTP. OTP Expired.", code=403)
                        else:
                            otp_obj.user.is_email_verified = True
                            otp_obj.user.save()
                            otp_obj.delete()
                            return Response(
                                {
                                    "status": True,
                                    "message": "OTP verified Successfully. Welcome to monorbit.",
                                },
                                status=200,
                            )
                    else:
                        raise ValidationError(detail="Invalid OTP", code=400)
                except acc_models.EmailVerifyOTP.DoesNotExist:
                    raise ValidationError(detail="Invalid OTP", code=400)
            else:
                raise ValidationError(detail="Unauthorized Request. Email address you entered is not accessible to your account.", code=403)
        else:
            raise ValidationError(detail="Please enter a valid email address.", code=400)