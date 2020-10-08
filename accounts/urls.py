from django.urls import path
from rest_framework_jwt.views import verify_jwt_token
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login_view'),
    path('logout/', LogoutView.as_view(), name='logout_view'),
    path('refresh-token/', RefreshToken.as_view(), name='refresh_token'),
    path('verify-token/', verify_jwt_token, name='verify_token'),
    path('user-info/<slug:mobile_number>/', GetUserInfo.as_view(), name='user_info'),
    path('delete-user/<slug:mobile_number>/', DeleteAccount.as_view(), name='delete_user'),
    path('register/', RegisterView.as_view(), name='register_view'),
    path('verify-mobile/', VerifyOTPView.as_view(), name='verify_mobile'),
    path('resend-mobile-otp/', ResendMobileVerifyOTPView.as_view(), name='resend_mobile_otp'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),

    path('sudo-mode/enter/', SudoModeAuthenticationView.as_view(), name='sudo_mode'),
    path('user-language/', UserLanguage.as_view(), name='user_language'),
]