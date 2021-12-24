from django.shortcuts import render
from django.db import connection
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Pass, Payment, Provider, Station, Vehicle

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