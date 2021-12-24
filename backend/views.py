from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Pass, Payment, Provider, Station, Vehicle
import csv


def all_vehicles_invalid():
	"""
	Makes all Vehicle entries invalid
	"""

	for v in Vehicle.objects.all():
		v.is_valid = 0
		v.save()


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