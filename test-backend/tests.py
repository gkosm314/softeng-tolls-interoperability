from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from backend.models import Pass, Station, Provider, Vehicle, Tag
from backend.backend import *
# Create your tests here.


class TestHardReset(TestCase):
    """
    Call the admin_hardreset() function and make sure that all the objects are inserted in the db
    """
    @classmethod
    def setUpTestData(cls):
        sample_csv = 'backend/test_data/test_sample_passes.csv'
        admin_hardreset(passes_csv=sample_csv)

    def test_passes_inserted(self):
        self.assertNotEqual(Pass.objects.all().count(), 0, 'There are no Passes in the db')

    def test_stations_inserted(self):
        self.assertNotEqual(Station.objects.all().count(), 0, 'There are no Stations in the db')

    def test_providers_inserted(self):
        self.assertNotEqual(Provider.objects.all().count(), 0, 'There are no Providers in the db')

    def test_vehicles_inserted(self):
        self.assertNotEqual(Vehicle.objects.all().count(), 0, 'There are no Vehicles in the db')

    def test_tags_inserted(self):
        self.assertNotEqual(Tag.objects.all().count(), 0, 'There are no Tags in the db')


class TestHealthCheck(TestCase):
    """
    Implements testing of the admin_healthcheck() functionality
    """
    def test_health_check(self):
        """
        Tests the expected status field of the Response and the status_code
        """
        response = admin_healthcheck()
        status = response.data['status']
        dbconnection = response.data['dbconnection']
        response_code = response.status_code
        if status == 'OK':
            """
            If the status returned is OK we are expecting to find a url in the dbconnection string\
            Check that it's not empty
            """
            self.assertNotEqual(status, '')
            self.assertEqual(response_code, 200)
        else:
            """
            Else check that the response string is 'failed' and reseponse_code is 500
            """
            self.assertEqual(status, 'failed')
            self.assertEqual(response_code, 500)
