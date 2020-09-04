from django.test import SimpleTestCase
from django.urls import reverse, resolve
from cart.views import *


class TestUrls(SimpleTestCase):
    """
    This class will test if all the urls are correctly mapped to their respective views
    """

    def test_create_url_is_resolved(self):
        url = reverse('cart:create')
        self.assertEquals(resolve(url).func.view_class, CreateCart)

    def test_update_url_is_resolved(self):
        url = reverse('cart:detail', args=['8hsdusd9'])
        self.assertEquals(resolve(url).func.view_class, UpdateCart)

    def test_all_url_is_resolved(self):
        url = reverse('cart:all')
        self.assertEquals(resolve(url).func.view_class, ListCart)

    def test_product_entry_create_url_is_resolved(self):
        url = reverse('cart:product_entry_create')
        self.assertEquals(resolve(url).func.view_class, CreateProductEntry)

    def test_product_entry_update_url_is_resolved(self):
        url = reverse('cart:product_entry_detail', args=[1])
        self.assertEquals(resolve(url).func.view_class, UpdateProductEntry)

    def test_product_entry_all_url_is_resolved(self):
        url = reverse('cart:product_entry_all')
        self.assertEquals(resolve(url).func.view_class, ListProductEntry)