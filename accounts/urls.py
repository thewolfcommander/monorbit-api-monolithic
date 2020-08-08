from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login_view'),
    path('logout/', LogoutView.as_view(), name='logout_view'),
    path('refresh-token/', RefreshToken.as_view(), name='refresh_token'),
    path('user-info/<slug:mobile_number>/', GetUserInfo.as_view(), name='user_info'),
    path('register/', RegisterView.as_view(), name='register_view'),
    path('verify-mobile/', VerifyOTPView.as_view(), name='verify_mobile'),
    path('resend-mobile-otp/', VerifyOTPView.as_view(), name='resend_mobile_otp'),
]