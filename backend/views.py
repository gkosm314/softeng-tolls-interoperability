from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Pass, Payment, Provider, Station, Vehicle

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