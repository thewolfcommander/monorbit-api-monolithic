from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import *


class TestUrls(SimpleTestCase):
    """
    This class will test if all the urls are correctly mapped to their respective views
    """

    def test_login_view_url_is_resolved(self):
        url = reverse('accounts:login_view')
        self.assertEquals(resolve(url).func.view_class, LoginView)
    
    def test_logout_view_url_is_resolved(self):
        url = reverse('accounts:logout_view')
        self.assertEquals(resolve(url).func.view_class, LogoutView)

    def test_refresh_token_url_is_resolved(self):
        url = reverse('accounts:refresh_token')
        self.assertEquals(resolve(url).func.view_class, RefreshToken)

    def test_user_info_url_is_resolved(self):
        url = reverse('accounts:user_info', args=['7253919169'])
        self.assertEquals(resolve(url).func.view_class, GetUserInfo)

    def test_delete_user_url_is_resolved(self):
        url = reverse('accounts:delete_user', args=['7253919169'])
        self.assertEquals(resolve(url).func.view_class, DeleteAccount)

    def test_register_view_url_is_resolved(self):
        url = reverse('accounts:register_view')
        self.assertEquals(resolve(url).func.view_class, RegisterView)

    def test_verify_mobile_url_is_resolved(self):
        url = reverse('accounts:verify_mobile')
        self.assertEquals(resolve(url).func.view_class, VerifyOTPView)

    def test_resend_mobile_otp_url_is_resolved(self):
        url = reverse('accounts:resend_mobile_otp')
        self.assertEquals(resolve(url).func.view_class, ResendMobileVerifyOTPView)

    def test_forgot_password_url_is_resolved(self):
        url = reverse('accounts:forgot_password')
        self.assertEquals(resolve(url).func.view_class, ForgotPasswordView)

    def test_reset_password_url_is_resolved(self):
        url = reverse('accounts:reset_password')
        self.assertEquals(resolve(url).func.view_class, ResetPasswordView)