from django.shortcuts import render
from django.contrib.auth import logout
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import generics
from .permissions import UserBelongsToProviderGroup

from backend.backend import admin_hardreset, admin_healthcheck, admin_resetpasses, admin_resetstations, admin_resetvehicles
from backend.backend import PassesPerStation, PassesAnalysis, PassesCost, ChargesBy


@api_view(['POST'])
def api_admin_hardreset(request, response_format = 'json'):
    """
	Deletes all the database entries and then re-inserts all the Providers, Stations, Vehicles and Passes.

	Note: this API call takes a lot of time to finish, since it inserts over 30000 passes in the database
    """
    
    #Calls equivelant API call from backend/backend.py
    return admin_hardreset(request, response_format)


@api_view(['GET'])
def api_admin_healthcheck(request, response_format = 'json'):
    """
	Ensures that we are connected to the database.
    """
    
    #Calls equivelant API call from backend/backend.py
    return admin_healthcheck(request, response_format)


@api_view(['POST'])
def api_admin_resetpasses(request, response_format = 'json'):
    """
	Deletes all Pass entries from the database, deletes all superusers and initializes a unique superuser.
    """
    
    #Calls equivelant API call from backend/backend.py
    return admin_resetpasses(request, response_format)


@api_view(['POST'])
def api_admin_resetstations(request, response_format = 'json'):
    """
	Flags all Station entries as invalid and then enters all the station in the sample data as valid stations.
    """
    
    #Calls equivelant API call from backend/backend.py
    return admin_resetstations(request, response_format)


@api_view(['POST'])
def api_admin_resetvehicles(request, response_format = 'json'):
    """
	Flags all Vehicle entries as invalid and then enters all the vehicles in the sample data as valid vehicles.
    """
    
    #Calls equivelant API call from backend/backend.py
    return admin_resetvehicles(request, response_format)


class LoginView(ObtainAuthToken):
	"""
	Perfroms user login.\n
	Returns a unique token the user will use to make API calls that require authentication.
	"""
	pass


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request, response_format = 'json'):
    """
	Performs user logout by making the user's token invalid.
    """

    try:
        request.user.auth_token.delete() # simply delete the token to force a login
    except (AttributeError):
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    logout(request)	#django built-in logout (django.contrib.auth)
    return Response(status=status.HTTP_200_OK)


api_authentication = [TokenAuthentication]
api_permissions = [IsAuthenticated, UserBelongsToProviderGroup]


class ApiPassesPerStation(PassesPerStation):
    """
	Returns a list with all the passes for a given stationID within a date range.
    """
    
    #Checks permissions and calls equivelant API call from backend/backend.py

    authentication_classes = api_authentication
    permission_classes = api_permissions


class ApiPassesAnalysis(PassesAnalysis):
    """
	Returns a list with all the passes from stations owned by operator 1 that were performed by vehicles with tags provided by operator 2 within a date range.\n
	Note: op1_ID and op2_ID are providerAbbr values.
    """
    
    #Checks permissions and calls equivelant API call from backend/backend.py

    authentication_classes = api_authentication
    permission_classes = api_permissions


class ApiPassesCost(PassesCost):
    """
	Returns the (aggregated) cost of passes from stations owned by operator 1 performed by vehicles with tags provided by operator 2 within a date range.\n
	Note: op1_ID and op2_ID are providerAbbr values.
    """
    
    #Checks permissions and calls equivelant API call from backend/backend.py

    authentication_classes = api_authentication
    permission_classes = api_permissions


class ApiChargesBy(ChargesBy):
    """
	Returns the amount each operator owes to the provided op_ID for a given date range.
    """
    
    #Checks permissions and calls equivelant API call from backend/backend.py

    authentication_classes = api_authentication
    permission_classes = api_permissions