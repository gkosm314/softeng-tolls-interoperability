from django.shortcuts import render
from rest_framework import status, serializers
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework import generics
from .permissions import UserBelongsToProviderGroup

from backend.backend import admin_hardreset, admin_healthcheck, admin_resetpasses, admin_resetstations, admin_resetvehicles
from backend.backend import PassesPerStation, PassesAnalysis, PassesCost, ChargesBy, LoginView, RefreshView
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample, extend_schema, OpenApiResponse, inline_serializer

@extend_schema (
    responses={
        200: inline_serializer(
            name='hardreset 200',
            fields= {
                'status': serializers.CharField(),
            }
        ),
        500: inline_serializer(
            name='hardreset 500',
            fields={
                'status': serializers.CharField(),
            }
        )
    },
    examples=[
        OpenApiExample(
            "Successful",
            description="An example of a successful endpoint call.",
            value={
                    "status": "OK",
                },
            response_only=True,
            status_codes=["200"],
        ),
        OpenApiExample(
            "Internal server error",
            description="Internal server error",
            value={
                "status": "failed",
            },
            response_only=True,
            status_codes=["500"]
        )
    ]
)
@api_view(['POST'])
def api_admin_hardreset(request, response_format = 'json'):
    """
	Deletes all the database entries and then re-inserts all the Providers, Stations, Vehicles and Passes.

	Note: this API call takes a lot of time to finish, since it inserts over 30000 passes in the database
    """
    
    #Calls equivelant API call from backend/backend.py
    return admin_hardreset(response_format)

@extend_schema (
    responses={
        200: inline_serializer(
            name='healthcheck 200',
            fields= {
                'status': serializers.CharField(),
                "dbconnection": serializers.CharField()
            }
        ),
        500: inline_serializer(
            name='healthcheck 500',
            fields={
                'status': serializers.CharField(),
                "dbconnection": serializers.CharField()
            }
        )
    },
    examples=[
        OpenApiExample(
            "Successful",
            description="An example of a successful endpoint call.",
            value={
                "status": "OK",
                "dbconnection": "mysql://tolls_root:tolls1234@127.0.0.1:3306/tolls_app_database"
            },
            response_only=True,
            status_codes=["200"],
        ),
        OpenApiExample(
            "Internal server error",
            description="Internal server error",
            value={
                "status": "failed",
                "dbconnection": "mysql://tolls_root:tolls1234@127.0.0.1:3306/tolls_app_database"
            },
            response_only=True,
            status_codes=["500"]
        )
    ]
)
@api_view(['GET'])
def api_admin_healthcheck(request, response_format = 'json'):
    """
	Ensures that we are connected to the database.
    """
    
    #Calls equivelant API call from backend/backend.py
    return admin_healthcheck(response_format)

@extend_schema (
    responses={
        200: inline_serializer(
            name='resetpasses 200',
            fields= {
                'status': serializers.CharField()
            }
        ),
        500: inline_serializer(
            name='resetpasses 500',
            fields={
                'status': serializers.CharField()
            }
        )
    },
    examples=[
        OpenApiExample(
            "Successful",
            description="An example of a successful endpoint call.",
            value={
                "status": "OK"
                },
            response_only=True,
            status_codes=["200"],
        ),
        OpenApiExample(
            "Internal server error",
            description="Internal server error",
            value={
                "status": "failed"
            },
            response_only=True,
            status_codes=["500"]
        )
    ]
)
@api_view(['POST'])
def api_admin_resetpasses(request, response_format = 'json'):
    """
	Deletes all Pass entries from the database, deletes all superusers and initializes a unique superuser.
    """
    
    #Calls equivelant API call from backend/backend.py
    return admin_resetpasses(response_format)

@extend_schema (
    responses={
        200: inline_serializer(
            name='resetstations 200',
            fields= {
                'status': serializers.CharField()
            }
        ),
        500: inline_serializer(
            name='resetstations 500',
            fields={
                'status': serializers.CharField()
            }
        )
    },
    examples=[
        OpenApiExample(
            "Successful",
            description="An example of a successful endpoint call.",
            value={
                "status": "OK"
                },
            response_only=True,
            status_codes=["200"],
        ),
        OpenApiExample(
            "Internal server error",
            description="Internal server error",
            value={
                "status": "failed"
            },
            response_only=True,
            status_codes=["500"]
        )
    ]
)
@api_view(['POST'])
def api_admin_resetstations(request, response_format = 'json'):
    """
	Flags all Station entries as invalid and then enters all the station in the sample data as valid stations.
    """
    
    #Calls equivelant API call from backend/backend.py
    return admin_resetstations(response_format)

@extend_schema (
    responses={
        200: inline_serializer(
            name='resetvehicles 200',
            fields= {
                'status': serializers.CharField()
            }
        ),
        500: inline_serializer(
            name='resetvehicles 500',
            fields={
                'status': serializers.CharField()
            }
        )
    },
    examples=[
        OpenApiExample(
            "Successful",
            description="An example of a successful endpoint call.",
            value={
                "status": "OK"
                },
            response_only=True,
            status_codes=["200"],
        ),
        OpenApiExample(
            "Internal server error",
            description="Internal server error",
            value={
                "status": "failed"
            },
            response_only=True,
            status_codes=["500"]
        )
    ]
)
@api_view(['POST'])
def api_admin_resetvehicles(request, response_format = 'json'):
    """
	Flags all Vehicle entries as invalid and then enters all the vehicles in the sample data as valid vehicles.
    """
    
    #Calls equivelant API call from backend/backend.py
    return admin_resetvehicles(response_format)


class ApiLoginView(LoginView):
	"""
	Perfroms user login.\n
	Returns a unique token the user will use to make API calls that require authentication.
	"""
	pass


@api_view(['POST'])
class ApiRefreshView(RefreshView):
    """
    Refreshes the lifetime of a token.
    """
    pass


api_permissions = [IsAuthenticated, UserBelongsToProviderGroup]


class ApiPassesPerStation(PassesPerStation):
    """
	Returns a list with all the passes for a given stationID within a date range.
    """
    
    #Checks permissions and calls equivelant API call from backend/backend.py

    permission_classes = api_permissions


class ApiPassesAnalysis(PassesAnalysis):
    """
	Returns a list with all the passes from stations owned by operator 1 that were performed by vehicles with tags provided by operator 2 within a date range.\n
	Note: op1_ID and op2_ID are providerAbbr values.
    """
    
    #Checks permissions and calls equivelant API call from backend/backend.py

    permission_classes = api_permissions


class ApiPassesCost(PassesCost):
    """
	Returns the (aggregated) cost of passes from stations owned by operator 1 performed by vehicles with tags provided by operator 2 within a date range.\n
	Note: op1_ID and op2_ID are providerAbbr values.
    """
    
    #Checks permissions and calls equivelant API call from backend/backend.py

    permission_classes = api_permissions


class ApiChargesBy(ChargesBy):
    """
	Returns the amount each operator owes to the provided op_ID for a given date range.
    """
    
    #Checks permissions and calls equivelant API call from backend/backend.py

    permission_classes = api_permissions