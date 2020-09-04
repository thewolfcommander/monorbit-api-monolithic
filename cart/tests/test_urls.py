from django.test import SimpleTestCase
from django.urls import reverse, resolve
from addresses.views import *


class TestUrls(SimpleTestCase):
    """
    This class will test if all the urls are correctly mapped to their respective views
    """

    def test_create_url_is_resolved(self):
        url = reverse('addresses:create')
        self.assertEquals(resolve(url).func.view_class, CreateAddress)

    def test_update_url_is_resolved(self):
        url = reverse('addresses:update', args=['8hsdusd9'])
        self.assertEquals(resolve(url).func.view_class, UpdateAddress)

    def test_all_url_is_resolved(self):
        url = reverse('addresses:all')
        self.assertEquals(resolve(url).func.view_class, ListAllAddresses)