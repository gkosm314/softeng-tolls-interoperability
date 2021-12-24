from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Pass, Payment, Provider, Station, Vehicle
import csv

def all_stations_invalid():
	"""
	Makes all Station entries invalid
	"""

	for s in Station.objects.all():
		s.is_valid = 0
		s.save()


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