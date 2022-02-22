import json

from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from backend.models import Pass, Station, Provider, Vehicle, Tag
from backend.backend import *
# Create your tests here.


sample_csv = 'test-backend/test-data/test_sample_passes.csv'


class TestHardReset(TestCase):
    """
    Call the admin_hardreset() function and make sure that all the objects are inserted in the db
    """
    @classmethod
    def setUpTestData(cls):
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
            Else check that the response string is 'failed' and response_code is 500
            """
            self.assertEqual(status, 'failed')
            self.assertEqual(response_code, 500)


class TestResetPasses(TestCase):
    """
    Implements testing of the admin_resetpasses functionality
    """
    def test_passes_are_deleted(self):
        """
        Inserts passes in the db and then calls admin_resetpasses to verify they are deleted
        """

        admin_hardreset(passes_csv=sample_csv)
        admin_resetpasses()
        self.assertEqual(Pass.objects.all().count(), 0)

    def test_superuser_is_deleted(self):
        """
        Makes sure the existing superusers are deleted after a call to admin_resetpasses
        """
        username = 'RandomSuperUser'
        # Insert a random superuser on the database
        User.objects.create_superuser(username, 'RandomSuperUser@email.com', 'RandomSuperUserPassword')
        user_exists = User.objects.filter(username=username).exists()
        self.assertTrue(user_exists)
        admin_resetpasses()
        # Make sure the superuser is deleted
        user_exists = User.objects.filter(username=username).exists()
        self.assertFalse(user_exists)

    def test_superuser_is_created(self):
        """
        Makes sure a superuser is created after a call to admin_resetpasses
        """
        username = 'admin'
        admin_resetpasses()
        # Make sure the superuser with name admin is created
        user_exists = User.objects.filter(username=username).exists()
        self.assertTrue(user_exists)


class TestResetStations(TestCase):
    """
    Implements testing of the admin_resetstations functionality
    """

    def test_all_stations_valid(self):
        """
        If we call admin_resetstations on an empty db then we should have only the stations we entered and therefore \
        they should be valid
        """
        insert_providers_from_csv()  # we need to insert the providers first because of foreign key constraints
        admin_resetstations()
        # Test that there are no invalid stations
        self.assertEqual(Station.objects.filter(isvalid=0).count(), 0)
        # Test that there are some valid stations to verify the call worked
        self.assertNotEqual(Station.objects.filter(isvalid=1).count(), 0)

    def test_station_becomes_invalid(self):
        """
        Insert a custom station that is not included in the csv file and make it valid
        admin_resetstations must make it invalid
        """
        insert_providers_from_csv()  # we need to insert the providers first because of foreign key constraints
        new_stationid = 'TestID'
        new_stationprovider = Provider.objects.all()[0]  # grab one provider
        new_stationname = 'TestNAME'

        new_station = Station(stationid=new_stationid, stationprovider=new_stationprovider, stationname=new_stationname,
                              isvalid=1)
        new_station.save()
        admin_resetstations()
        self.assertEqual(Station.objects.get(stationid=new_stationid).isvalid, 0)


class TestResetVehicles(TestCase):
    """
    Implements testing of the admin_resetstations functionality
    """

    def test_all_vehciles_valid(self):
        """
        If we call admin_resetvehicles on an empty db then we should have only the stations we entered and therefore \
        they should be valid
        """
        insert_providers_from_csv()  # we need to insert the providers first because of foreign key constraints
        admin_resetvehicles()
        # Test that there are no invalid stations
        self.assertEqual(Vehicle.objects.filter(isvalid=0).count(), 0)
        # Test that there are some valid stations to verify the call worked
        self.assertNotEqual(Vehicle.objects.filter(isvalid=1).count(), 0)

    def test_station_becomes_invalid(self):
        """
        Insert a custom vehicle that is not included in the csv file and make it valid
        admin_resetvehicles must make it invalid
        """
        insert_providers_from_csv()  # we need to insert the providers first because of foreign key constraints
        new_providerabbr = Provider.objects.all()[0]
        new_tagid = 'TestTag'
        new_tagprovider = str(new_providerabbr)
        new_tag = Tag(tagid=new_tagid, tagprovider=new_tagprovider)
        new_tag.save()
        new_vehicleid = 'TestVehicle'
        new_licenceyear = 1900
        new_vehicle = Vehicle(vehicleid=new_vehicleid, tag=new_tag, providerabbr=new_providerabbr,
                              licenseyear=new_licenceyear, isvalid=1)
        new_vehicle.save()
        admin_resetvehicles()
        self.assertEqual(Vehicle.objects.get(vehicleid=new_vehicleid).isvalid, 0)


class TestPassesPerStation(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Call admin_hardreset in order to put the sample data in the database
        """
        admin_hardreset(passes_csv=sample_csv)
        return

    def test_response_returned(self):
        """
        Generate a request using on the /interoperability/api/PassesPerStation/ view and verify that the output
        is the one expected
        Assumes that the correct output already exists on the file test-backend/test-data/PassesPerStation_expected.json
        with the only change being the RequestTimestamp field which must be set to 'REQUEST_TIMESTAMP'
        """
        factory = RequestFactory()
        station = 'OO01'
        datefrom = '20190102'
        dateto = '20190105'
        with open('test-backend/test-data/PassesPerStation_expected.json', 'r') as f:
            expected_result = json.load(f)
        request_path = f"/interoperability/api/PassesPerStation/{station}/{datefrom}/{dateto}"
        request = factory.get(request_path)
        response = PassesPerStation.as_view()(request, stationID=station, datefrom=datefrom, dateto=dateto)
        # Check that the response is not None
        self.assertIsNotNone(response)
        # Check that the response object is indeed of type Response
        self.assertEqual(type(response), Response)
        response.data['RequestTimestamp'] = "REQUEST_TIMESTAMP"
        # This field is ignored because it depends on the time of the request
        self.assertJSONEqual(json.dumps(response.data, default=str), expected_result)