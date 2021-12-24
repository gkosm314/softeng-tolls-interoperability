from django.shortcuts import render
from django.db import transaction, connection
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Pass, Payment, Provider, Station, Vehicle
import csv
from datetime import datetime


def all_stations_invalid():
	"""
	Makes all Station entries invalid
	"""

	for s in Station.objects.all():
		s.is_valid = 0
		s.save()


def all_vehicles_invalid():
	"""
	Makes all Vehicle entries invalid
	"""

	for v in Vehicle.objects.all():
		v.is_valid = 0
		v.save()


def update_station_from_csv_line(row):
	"""
	Inserts a Station entry into the database. If an entry with the same primary key already exists, it updates it accordingly.

	Parameters: 
		-row: a csv line from a csv.reader that reads stations_csv_path
	"""

	new_stationid = row[0]
	new_stationprovider = Provider.objects.get(providername = row[1])
	new_stationname = row[2]

	new_station = Station(stationid = new_stationid, stationprovider = new_stationprovider, stationname = new_stationname, isvalid = 1)
	new_station.save()


def update_vehicle_from_csv_line(row):
	"""
	Inserts a Vehicle entry into the database. If an entry with the same primary key already exists, it updates it accordingly.

	Parameters: 
		-row: a csv line from a csv.reader that reads vehicle_csv_path
	"""

	new_vehicleid = row[0]
	new_tagid = row[1]
	new_tagprovider = row[2]
	new_providerabbr = Provider.objects.get(providerabbr = row[3])
	new_licenceyear = row[4]

	new_station = Vehicle(vehicleid = new_vehicleid, tagid = new_tagid, tagprovider = new_tagprovider, providerabbr = new_providerabbr, licenseyear = new_licenceyear, isvalid = 1)
	new_station.save()


def update_provider_from_csv_line(row):
	"""
	Inserts a Provider entry into the database. If an entry with the same primary key already exists, it updates it accordingly.

	Parameters: 
		-row: a csv line from a csv.reader that reads providers_csv_path
	"""

	new_providerid = row[0]
	new_providername = row[1]
	new_providerabbr = row[2]

	new_provider = Provider(providerid = new_providerid, providername = new_providername, providerabbr = new_providerabbr, isvalid = 1)
	new_provider.save()


def update_pass_from_csv_line(row):	
	"""
	Inserts a Pass entry into the database. If an entry with the same primary key already exists, it updates it accordingly.

	Parameters: 
		-row: a csv line from a csv.reader that reads passes_csv_path
	"""

	new_passid = row[0]
	new_timestamp = datetime.strptime(row[1], "%d/%m/%Y %H:%M") #string to datetime python object (python built-in datetime library)
	new_stationref = Station.objects.get(stationid = row[2])
	new_vehicleref = Vehicle.objects.get(vehicleid = row[3])
	new_providerabbr = new_stationref.stationprovider;
	new_charge = row[4]

	#If you passed from a provider's stations using said provider's tag, then the pass is a home pass
	new_ishome = (new_providerabbr.providerid == new_stationref.stationprovider)

	new_pass = Pass(passid = new_passid, timestamp = new_timestamp, stationref = new_stationref, vehicleref = new_vehicleref, charge = new_charge, providerabbr = new_providerabbr, ishome = new_ishome)
	new_pass.save()


@api_view(['POST'])
def admin_hardreset(request, response_format = 'json'):
	"""
	Implements /admin/hardreset API call. Admin authentication required.
	Deletes all the database entries and then re-inserts all the Providers, Stations, Vehicles and Passes.

	Important note: this API call takes a lot of time to finish, since it inserts over 30000 passes in the database
	"""	

	#Read sample data from csv file located at the following paths
	stations_csv_path = 'backend/sample_data/sampledata01_stations.csv'
	vehicles_csv_path = 'backend/sample_data/sampledata01_vehicles_100.csv'
	providers_csv_path = 'backend/sample_data/sampledata01_providers.csv'
	passes_csv_path = 'backend/sample_data/sampledata01_passes100_8000.csv'

	with transaction.atomic():
		#Delete everything
		Provider.objects.all().delete()
		Station.objects.all().delete()
		Vehicle.objects.all().delete()
		Pass.objects.all().delete()
		Payment.objects.all().delete()

		#Insert providers
		with open(providers_csv_path) as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=';')

			#Skip first line(headers)
			next(csv_reader)

			#Process each line
			for row in csv_reader:
				try:
					update_provider_from_csv_line(row)
				except Exception as e:
					raise e
					return Response({"status": "failed"}, status.HTTP_500_INTERNAL_SERVER_ERROR)

		#Insert stations
		with open(stations_csv_path) as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=';')

			#Skip first line(headers)
			next(csv_reader)

			#Process each line
			for row in csv_reader:
				try:
					update_station_from_csv_line(row)
				except Exception as e:
					print(row)
					raise e
		# 			return Response({"status": "failed"}, status.HTTP_500_INTERNAL_SERVER_ERROR)

		#Insert vehicles
		with open(vehicles_csv_path) as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=';')

			#Skip first line(headers)
			next(csv_reader)

			#Process each line
			for row in csv_reader:
				try:
					update_vehicle_from_csv_line(row)
				except Exception as e:
					raise e
					return Response({"status": "failed"}, status.HTTP_500_INTERNAL_SERVER_ERROR)

		# #Insert passes
		# with open(passes_csv_path) as csv_file:
		# 	csv_reader = csv.reader(csv_file, delimiter=';')

		# 	#Skip first line(headers)
		# 	next(csv_reader)

		# 	#Process each line
		# 	for row in csv_reader:
		# 		try:
		# 			update_pass_from_csv_line(row)
		# 			print(row)
		# 		except Exception as e:
		# 			raise e
		# 			return Response({"status": "failed"}, status.HTTP_500_INTERNAL_SERVER_ERROR)

	return Response({"status": "OK"}, status.HTTP_200_OK)


@api_view(['GET'])
def admin_healthcheck(request, response_format = 'json'):
	"""
	Implements /admin/healthcheck API call. Admin authentication required.
	Ensures that we are connected to the database.
	"""

	connection_string = "mysql://tolls_root:tolls1234@127.0.0.1:3306/tolls_app_database"; 
	try:
		connection.ensure_connection()
	except Exception as e:
		return Response({"status": "failed", "dbconnection": connection_string}, status.HTTP_500_INTERNAL_SERVER_ERROR)
	else:
		return Response({"status": "OK", "dbconnection": connection_string}, status.HTTP_200_OK)


def initialize_super_user():
	"""
	Deletes all superusers and creates a new one with the default admin password
	"""

	#Delete all superusers
	for u in User.objects.filter(is_superuser=True):
		u.delete()

	#Initialize a super user
	new_superuser = User(username = 'admin')
	new_superuser.set_password('freepasses4all')
	new_superuser.is_superuser = True
	new_superuser.is_staff = True
	new_superuser.save()


@api_view(['POST'])
def admin_resetpasses(request, response_format = 'json'):
	"""
	Implements /admin/resetpasses API call. Admin authentication required.
	Deletes all Pass entries from the database and initializes a unique superuser
	"""

	try:
		Pass.objects.all().delete()
	except Exception as e:
		return Response({"status": "failed"}, status.HTTP_500_INTERNAL_SERVER_ERROR)

	try:
		initialize_super_user()
	except Exception as e:
		return Response({"status": "failed"}, status.HTTP_500_INTERNAL_SERVER_ERROR)
	
	return Response({"status": "OK"}, status.HTTP_200_OK)


@api_view(['POST'])
def admin_resetstations(request, response_format = 'json'):
	"""
	Implements /admin/resetstations API call. Admin authentication required.
	Marks all Station entries as invalid and then enters all the station in the sample data as valid stations.
	"""

	#Read sample data from csv file located at the following paths
	stations_csv_path = 'backend/sample_data/sampledata01_stations.csv'

	try:
		all_stations_invalid()
	except Exception as e:
		return Response({"status": "failed"}, status.HTTP_500_INTERNAL_SERVER_ERROR)

	with open(stations_csv_path) as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=';')

			#Skip first line(headers)
			next(csv_reader)

			#Process each line
			for row in csv_reader:			
				try:
					update_station_from_csv_line(row)
				except Exception as e:
					return Response({"status": "failed"}, status.HTTP_500_INTERNAL_SERVER_ERROR)
			
	return Response({"status": "OK"}, status.HTTP_200_OK)


@api_view(['POST'])
def admin_resetvehicles(request, response_format = 'json'):
	"""
	Implements /admin/resetvehicles API call. Admin authentication required.
	Marks all Vehicle entries as invalid and then enters all the vehicles in the sample data as valid vehicles.
	"""
	
	#Read sample data from csv file located at the following paths
	vehicles_csv_path = 'backend/sample_data/sampledata01_vehicles_100.csv'

	try:
		all_vehicles_invalid()
	except Exception as e:
		return Response({"status": "failed"}, status.HTTP_500_INTERNAL_SERVER_ERROR)

	with open(vehicles_csv_path) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=';')

		#Skip first line(headers)
		next(csv_reader)

		#Process each line
		for row in csv_reader:
			try:
				update_vehicle_from_csv_line(row)
			except Exception as e:
				return Response({"status": "failed"}, status.HTTP_500_INTERNAL_SERVER_ERROR)

	return Response({"status": "OK"}, status.HTTP_200_OK)	