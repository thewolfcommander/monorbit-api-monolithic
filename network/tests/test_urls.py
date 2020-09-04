from django.test import SimpleTestCase
from django.urls import reverse, resolve
from job_profiles.views import *


class TestUrls(SimpleTestCase):
    """
    This class will test if all the urls are correctly mapped to their respective views
    """

    def test_all_profiles_url_is_resolved(self):
        url = reverse('job_profiles:all_profiles')
        self.assertEquals(resolve(url).func.view_class, ListCreateJobProfile)

    def test_update_profiles_url_is_resolved(self):
        url = reverse('job_profiles:update_profiles', args=['8hsdusd9'])
        self.assertEquals(resolve(url).func.view_class, UpdateJobProfile)

    def test_dboy_vehicle_all_url_is_resolved(self):
        url = reverse('job_profiles:dboy_vehicle_all')
        self.assertEquals(resolve(url).func.view_class, ListCreateDeliveryBoyVehicle)

    def test_dboy_vehicle_update_url_is_resolved(self):
        url = reverse('job_profiles:dboy_vehicle_update', args=['89s8jdjs'])
        self.assertEquals(resolve(url).func.view_class, UpdateDeliveryBoyVehicle)

    def test_dboy_all_url_is_resolved(self):
        url = reverse('job_profiles:dboy_all')
        self.assertEquals(resolve(url).func.view_class, ListDeliveryBoys)

    def test_dboy_create_url_is_resolved(self):
        url = reverse('job_profiles:dboy_create')
        self.assertEquals(resolve(url).func.view_class, CreateDeliveryBoys)

    def test_dboy_update_url_is_resolved(self):
        url = reverse('job_profiles:dboy_update', args=['9ns8sjxs'])
        self.assertEquals(resolve(url).func.view_class, UpdateDeliveryBoy)
    
    def test_permanent_all_url_is_resolved(self):
        url = reverse('job_profiles:permanent_all')
        self.assertEquals(resolve(url).func.view_class, ListPermanentEmployee)

    def test_permanent_create_url_is_resolved(self):
        url = reverse('job_profiles:permanent_create')
        self.assertEquals(resolve(url).func.view_class, CreatePermanentEmployee)

    def test_permanent_update_url_is_resolved(self):
        url = reverse('job_profiles:permanent_update', args=['98nsj8s9'])
        self.assertEquals(resolve(url).func.view_class, UpdatePermanentEmployee)

    def test_freelancer_all_url_is_resolved(self):
        url = reverse('job_profiles:freelancer_all')
        self.assertEquals(resolve(url).func.view_class, ListFreelancer)

    def test_freelancer_create_url_is_resolved(self):
        url = reverse('job_profiles:freelancer_create')
        self.assertEquals(resolve(url).func.view_class, CreateFreelancer)

    def test_freelancer_update_url_is_resolved(self):
        url = reverse('job_profiles:freelancer_update', args=['989sj9s'])
        self.assertEquals(resolve(url).func.view_class, UpdateFreelancer)