from dataclasses import fields
from unicodedata import name
from django.shortcuts import render
from django.db import transaction, connection
from django.contrib.auth.models import User
from django.contrib.auth import logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import Pass, Provider, Station, Vehicle, Tag
import csv
from datetime import datetime
from .serializers import PassSerializer_PassesPerStation, PassSerializer_PassesAnalysis ,StationSerializer
from rest_framework import generics, serializers
from django.db.models import Sum
from . import examples

from drf_spectacular.utils import extend_schema_serializer, OpenApiExample, extend_schema, OpenApiResponse, inline_serializer, PolymorphicProxySerializer, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

#Note: Django REST Framework's Response object can handle both JSON and CSV responses

#Read sample data from csv file located at the following paths
stations_csv_path = 'backend/sample_data/sampledata01_stations.csv'
vehicles_csv_path = 'backend/sample_data/sampledata01_vehicles_100.csv'
providers_csv_path = 'backend/sample_data/sampledata01_providers.csv'
passes_csv_path = 'backend/sample_data/sampledata01_passes100_8000.csv'


def all_stations_invalid():
    """
    Makes all Station entries invalid
    """

    for s in Station.objects.all():
        s.isvalid = 0
        s.save()


def all_vehicles_invalid():
    """
    Makes all Vehicle entries invalid
    """

    for v in Vehicle.objects.all():
        v.isvalid = 0
        v.save()

    for t in Tag.objects.all():
        t.isvalid = 0
        t.save()


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

    new_tagid = row[1]
    new_tagprovider = row[2]

    new_tag = Tag(tagid = new_tagid, tagprovider = new_tagprovider)
    new_tag.save()

    new_vehicleid = row[0]
    new_providerabbr = Provider.objects.get(providerabbr = row[3])
    new_licenceyear = row[4]

    new_vehicle = Vehicle(vehicleid = new_vehicleid, tag = new_tag, providerabbr = new_providerabbr, licenseyear = new_licenceyear, isvalid = 1)
    new_vehicle.save()


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
    new_charge = row[4]

    #If you passed from a provider's stations using said provider's tag, then the pass is a home pass
    new_providerabbr = new_stationref.stationprovider
    new_ishome = (new_providerabbr.providerid == new_vehicleref.providerabbr.providerid)

    new_pass = Pass(passid = new_passid, timestamp = new_timestamp, stationref = new_stationref, vehicleref = new_vehicleref, charge = new_charge, ishome = new_ishome)
    new_pass.save()


def admin_hardreset(response_format = 'json'):
    """
    Implements /admin/hardreset API call.
    Deletes all the database entries and then re-inserts all the Providers, Stations, Vehicles and Passes.

    Important note: this API call takes a lot of time to finish, since it inserts over 30000 passes in the database
    """

    with transaction.atomic():
        #Delete everything
        Provider.objects.all().delete()
        Station.objects.all().delete()
        Vehicle.objects.all().delete()
        Tag.objects.all().delete()
        Pass.objects.all().delete()
        #Payment.objects.all().delete()

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
                    return Response({"status": "failed"}, status.HTTP_500_INTERNAL_SERVER_ERROR)

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
                    print(e)
                    return Response({"status": "failed"}, status.HTTP_500_INTERNAL_SERVER_ERROR)

        #Insert passes
        with open(passes_csv_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')

            #Skip first line(headers)
            next(csv_reader)

            #Process each line
            for row in csv_reader:
                try:
                    update_pass_from_csv_line(row)
                    print(row)
                except Exception as e:
                    return Response({"status": "failed"}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"status": "OK"}, status.HTTP_200_OK)


def admin_healthcheck(response_format = 'json'):
    """
    Implements /admin/healthcheck API call.
    Ensures that we are connected to the database.
    """

    connection_string = "mysql://tolls_root:tolls1234@127.0.0.1:3306/tolls_app_database"; #?
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


def admin_resetpasses(response_format = 'json'):
    """
    Implements /admin/resetpasses API call.
    Deletes all Pass entries from the database,deletes all superusers and initializes a unique superuser.
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


def admin_resetstations(response_format = 'json'):
    """
    Implements /admin/resetstations API call.
    Marks all Station entries as invalid and then enters all the station in the sample data as valid stations.
    """

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


def admin_resetvehicles(response_format = 'json'):
    """
    Implements /admin/resetvehicles API call.
    Marks all Vehicle entries as invalid and then enters all the vehicles in the sample data as valid vehicles.
    """

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


class LoginView(TokenObtainPairView):
    pass


class RefreshView(TokenRefreshView):
    pass


def get_datetime_from_kwarg(kwarg_date: str) -> datetime:
    """
    Returns a datetime object from the kwarg_date provided
    The expected format for kwarg_date is YYYYMMDD
    """
    return datetime.strptime(kwarg_date, '%Y%m%d')


class PassesPerStation(generics.ListAPIView):
    """
    Return a list with all the passes for a given stationID and date range
    """

    serializer_class = PassSerializer_PassesPerStation
    invalid_request_response = Response({"status": "failed"}, status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        station_id = self.kwargs['stationID']
        date_from = get_datetime_from_kwarg(self.kwargs['datefrom']).date()
        date_to = get_datetime_from_kwarg(self.kwargs['dateto']).date()
        return Pass.objects.filter(stationref__stationid=station_id, timestamp__lte=date_to, timestamp__gte=date_from)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
        except Exception as e:
            print(e)
            return self.invalid_request_response
        page = self.paginate_queryset(queryset)
        station_id = self.kwargs['stationID']
        date_from = get_datetime_from_kwarg(self.kwargs['datefrom']).date()
        date_to = get_datetime_from_kwarg(self.kwargs['dateto']).date()
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
        try:
            station = Station.objects.get(stationid=station_id)
        except Exception as e:
            # TODO: Decide if we need to return 500 or 400 error codes when an invalid param is passed eg here
            return self.invalid_request_response
        station_provider = station.stationprovider.providername
        response_data = {
            'Station': station_id,
            'StationOperator': station_provider,
            'RequestTimestamp': time_now,
            'PeriodFrom': date_from,
            'PeriodTo': date_to,
            'NumberOfPasses': len(data),
            'PassesList': data
        }
        """
        Check if there is no data, then return the same format but with 402 Response code
        Returning the same format instead of eg an empty body is an implementation decision and can be changed if 
        required by simply setting response_data to whatever the response should be
        """
        if len(data) == 0:
            response_code = status.HTTP_402_PAYMENT_REQUIRED
        else:
            response_code = status.HTTP_200_OK
        return Response(response_data, status=response_code)

    @extend_schema (
        parameters=[
            OpenApiParameter(
                name='datefrom',
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.PATH,
                description='Date format: yyyymmdd',
                examples=[
                    OpenApiExample(
                        'Date example',
                        #summary='short optional summary',
                        #description='longer description',
                        value='20200423'
                    )                  
                ]
            ),
        ],
        responses={
            200: inline_serializer(
                name='PassesPerStation 200',
                fields={
                    'Station': serializers.CharField(),
                    'StationOperator': serializers.CharField(),
                    'RequestTimestamp': serializers.DateTimeField(),
                    'PeriodFrom': serializers.DateField(),
                    'PeriodTo':  serializers.DateField(),
                    'NumberOfPasses': serializers.IntegerField(),
                    'PassesList': PassSerializer_PassesPerStation()
               }
            ),
            400: inline_serializer(
                name='PassesPerStation 400',
                fields={
                    'status': serializers.CharField()
                }
            ),
            401: PolymorphicProxySerializer(
                component_name='Status code 401',
                serializers=[
                    inline_serializer(
                        name="401 No credentials",
                        fields={
                            "detail": serializers.CharField()
                        }
                    ),
                    inline_serializer(
                        name='401 Invalid Token',
                        fields={
                            "detail": serializers.CharField(),
                            "code": serializers.CharField(),
                            "messages": inline_serializer(
                                name="messages",
                                fields={
                                    "token_class": serializers.CharField(),
                                    "token_type": serializers.CharField(),
                                    "message": serializers.CharField()
                                }
                            )
                        }
                    )
                ],
                resource_type_field_name= None,
            ),
            500: inline_serializer(
                name='PassesPerStation 500',
                fields={
                    'status': serializers.CharField()
                }
            )
        },
        examples=[
            OpenApiExample(
                "Successful",
                description="An example of a successful endpoint call.",
                value=examples.ourdict["PassesPerStation"],
                response_only=True,
                status_codes=["200"],
            ),
            OpenApiExample(
                "Bad request",
                description="An example of a failed endpoint call due to bad request.",
                value={"status": "failed"},
                response_only=True,
                status_codes=["400"],
            ),
            OpenApiExample(
                "No credentials",
                description="Output when credentials are not provided.",
                value=examples.ourdict["Unauthorized_noCredentials"],
                response_only=True,
                status_codes=["401"]
            ),
            OpenApiExample(
                "Invalid Token",
                description="Token is invalid.",
                value=examples.ourdict["Unauthorized_invalidToken"],
                response_only=True,
                status_codes=["401"]
            ),
            OpenApiExample(
                "Internal server error",
                description="Internal server error",
                value={"status": "failed"},
                response_only=True,
                status_codes=["500"]
            )

        ],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PassesAnalysis(generics.ListAPIView):
    """
        Return all the passes on stations of op1 from vehicles with tags of op2

        Assuming op1_ID and op2_ID are the providerAbbr fields
    """

    serializer_class = PassSerializer_PassesAnalysis
    invalid_request_response = Response({"status": "failed"}, status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        """
            Return all the passes on stations of op1 from vehicles with tags of op2
            Assuming op1_ID and op2_ID are the providerAbbr fields
        """
        op1_id_from_request = self.kwargs['op1_ID']
        op2_id_from_request = self.kwargs['op2_ID']
        """
            Grab corresponding ids for operators from user params
            Only change in case the params from the user are not the providerAbbr must be made here, the rest of the code
            will work just fine once the op1_id and op2_id variables are correctly set to the pk
        """
        op1_id = (Provider.objects.get(providerabbr=op1_id_from_request)).providerid
        op2_id = (Provider.objects.get(providerabbr=op2_id_from_request)).providerid

        date_from = get_datetime_from_kwarg(self.kwargs['datefrom']).date()
        date_to = get_datetime_from_kwarg(self.kwargs['dateto']).date()
        # Find all the vehicles with tags of op2
        op2_vehicles = Vehicle.objects.filter(providerabbr=op2_id)
        # Find all the stations with tags of op1
        op1_stations = Station.objects.filter(stationprovider=op1_id)
        qs = Pass.objects.filter(timestamp__lte=date_to, timestamp__gte=date_from, stationref__in=op1_stations, vehicleref__in=op2_vehicles)
        return qs

    def list(self, request, *args, **kwargs):
        """
            Overwrite the method to add custom values to the response
        """
        try:
            queryset = self.filter_queryset(self.get_queryset())
        except Exception as e:
            return self.invalid_request_response
        page = self.paginate_queryset(queryset)
        op1_id_from_request = self.kwargs['op1_ID']
        op2_id_from_request = self.kwargs['op2_ID']
        date_from = get_datetime_from_kwarg(self.kwargs['datefrom']).date()
        date_to = get_datetime_from_kwarg(self.kwargs['dateto']).date()
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
        response_data = {
            'op1_ID': op1_id_from_request,
            'op2_ID': op2_id_from_request,
            'RequestTimestamp': time_now,
            'PeriodFrom': date_from,
            'PeriodTo': date_to,
            'NumberOfPasses': len(data),
            'PassesList': data
        }
        """
        Check if there is no data, then return the same format but with 402 Response code
        Returning the same format instead of eg an empty body is an implementation decision and can be changed if 
        required by simply setting response_data to whatever the response should be
        """
        if len(data) == 0:
            response_code = status.HTTP_402_PAYMENT_REQUIRED
        else:
            response_code = status.HTTP_200_OK
        return Response(response_data, status=response_code)

    @extend_schema (
        responses={
            200: inline_serializer(
                name='PassesAnalysis 200',
                fields= {
                    'op1_ID': serializers.CharField(),
                    'op2_ID': serializers.CharField(),
                    'RequestTimestamp': serializers.DateTimeField(),
                    'PeriodFrom': serializers.DateField(),
                    'PeriodTo':  serializers.DateField(),
                    'NumberOfPasses': serializers.IntegerField(),
                    'PassesList': PassSerializer_PassesAnalysis()
               }
            ),
            400: inline_serializer(
                name='PassesAnalysis 400',
                fields={
                    'status': serializers.CharField()
                }
            ),
            401: PolymorphicProxySerializer(
                component_name='Status code 401',
                serializers=[
                    inline_serializer(
                        name="401 No credentials",
                        fields={
                         "detail": serializers.CharField()
                        }
                    ),
                    inline_serializer(
                        name='401 Invalid Token',
                        fields={
                            "detail": serializers.CharField(),
                            "code": serializers.CharField(),
                            "messages": inline_serializer(
                                name="messages",
                                fields={
                                    "token_class": serializers.CharField(),
                                    "token_type": serializers.CharField(),
                                    "message": serializers.CharField()
                                }
                            )
                        }
                    )
                ],
                resource_type_field_name= None,
            ),
            500: inline_serializer(
                name='PassesAnalysis 500',
                fields={
                    'status': serializers.CharField()
                }
            )
        },
        examples=[
            OpenApiExample(
                "Successful",
                description="An example of a successful endpoint call.",
                value=examples.ourdict["PassesAnalysis"],
                response_only=True,
                status_codes=["200"],
            ),
            OpenApiExample(
                "Bad request",
                description="An example of a failed endpoint call due to bad request.",
                value={"status": "failed"},
                response_only=True,
                status_codes=["400"],
            ),
            OpenApiExample(
                "No credentials",
                description="Output when credentials are not provided.",
                value=examples.ourdict["Unauthorized_noCredentials"],
                response_only=True,
                status_codes=["401"]
            ),
            OpenApiExample(
                "Invalid Token",
                description="Token is invalid.",
                value=examples.ourdict["Unauthorized_invalidToken"],
                response_only=True,
                status_codes=["401"]
            ),
            OpenApiExample(
                "Internal server error",
                description="Internal server error",
                value={"status": "failed"},
                response_only=True,
                status_codes=["500"]
            )
        ],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PassesCost(generics.ListAPIView):
    """
        Return the (aggregated) cost of passes on stations of op1 from vehicles with tags of op2

        Assuming op1_ID and op2_ID are the providerAbbr fields
    """
    """
        This could be another form of generics ApiView, leaving it as it is because it is very similar
        to the PassesAnalysis one (even though there is no listing involved in the Response)
    """

    serializer_class = PassSerializer_PassesAnalysis
    invalid_request_response = Response({"status": "failed"}, status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        """
            Return the (aggregated) cost of passes on stations of op1 from vehicles with tags of op2
            Assuming op1_ID and op2_ID are the providerAbbr fields
        """
        op1_id_from_request = self.kwargs['op1_ID']
        op2_id_from_request = self.kwargs['op2_ID']
        """
            Grab corresponding ids for operators from user params
            Only change in case the params from the user are not the providerAbbr must be made here, the rest of the code
            will work just fine once the op1_id and op2_id variables are correctly set to the pk
        """
        op1_id = (Provider.objects.get(providerabbr=op1_id_from_request)).providerid
        op2_id = (Provider.objects.get(providerabbr=op2_id_from_request)).providerid
        date_from = get_datetime_from_kwarg(self.kwargs['datefrom']).date()
        date_to = get_datetime_from_kwarg(self.kwargs['dateto']).date()
        # Find all the vehicles with tags of op2
        op2_vehicles = Vehicle.objects.filter(providerabbr=op2_id)
        # Find all the stations with tags of op1
        op1_stations = Station.objects.filter(stationprovider=op1_id)
        qs = Pass.objects.filter(timestamp__lte=date_to, timestamp__gte=date_from, stationref__in=op1_stations, vehicleref__in=op2_vehicles)
        return qs


    def list(self, request, *args, **kwargs):
        """
            Overwrite the method to add custom values to the response
        """
        try:
            queryset = self.filter_queryset(self.get_queryset())
        except Exception as e:
            return self.invalid_request_response
        price = queryset.aggregate(Sum('charge'))['charge__sum']
        page = self.paginate_queryset(queryset)
        op1_id_from_request = self.kwargs['op1_ID']
        op2_id_from_request = self.kwargs['op2_ID']
        date_from = get_datetime_from_kwarg(self.kwargs['datefrom']).date()
        date_to = get_datetime_from_kwarg(self.kwargs['dateto']).date()
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
        if len(data) == 0:
            price = 0
        response_data = {
            'op1_ID': op1_id_from_request,
            'op2_ID': op2_id_from_request,
            'RequestTimestamp': time_now,
            'PeriodFrom': date_from,
            'PeriodTo': date_to,
            'NumberOfPasses': len(data),
            'PassesCost': price
        }
        """
        Check if there is no data, then return the same format but with 402 Response code
        Returning the same format instead of eg an empty body is an implementation decision and can be changed if 
        required by simply setting response_data to whatever the response should be
        """
        if len(data) == 0:
            response_code = status.HTTP_402_PAYMENT_REQUIRED
        else:
            response_code = status.HTTP_200_OK
        return Response(response_data, status=response_code)

    @extend_schema (
        responses={
            200: inline_serializer(
                name='PassesCost 200',
                fields= {
                    'op1_ID': serializers.CharField(),
                    'op2_ID': serializers.CharField(),
                    'RequestTimestamp': serializers.DateTimeField(),
                    'PeriodFrom': serializers.DateField(),
                    'PeriodTo':  serializers.DateField(),
                    'NumberOfPasses': serializers.IntegerField(),
                    'PassesCost': serializers.IntegerField()
                }
            ),
            400: inline_serializer(
                name='PassesCost 400',
                fields={
                    'status': serializers.CharField()
                }
            ),
            401: PolymorphicProxySerializer(
                component_name='Status code 401',  
                serializers=[
                    inline_serializer(
                        name="401 No credentials",
                        fields={
                         "detail": serializers.CharField()
                        }
                    ),
                    inline_serializer(
                        name='401 Invalid Token',
                        fields={
                            "detail": serializers.CharField(),
                            "code": serializers.CharField(),
                            "messages": inline_serializer(
                                name="messages",
                                fields={
                                    "token_class": serializers.CharField(),
                                    "token_type": serializers.CharField(),
                                    "message": serializers.CharField()
                                }
                            )
                        }
                    )
                ],
                resource_type_field_name= None,
            ),
            500: inline_serializer(
                name='PassesCost 500',
                fields={
                    'status': serializers.CharField()
                }
            )
        },
        examples=[
            OpenApiExample(
                "Successful",
                description="An example of a successful endpoint call.",
                value=examples.ourdict["PassesCost"],
                response_only=True,
                status_codes=["200"],
            ),
            OpenApiExample(
                "Bad request",
                description="An example of a failed endpoint call due to bad request.",
                value={"status": "failed"},
                response_only=True,
                status_codes=["400"],
            ),
            OpenApiExample(
                "No credentials",
                description="Output when credentials are not provided.",
                value=examples.ourdict["Unauthorized_noCredentials"],
                response_only=True,
                status_codes=["401"]
            ),
            OpenApiExample(
                "Invalid Token",
                description="Token is invalid.",
                value=examples.ourdict["Unauthorized_invalidToken"],
                response_only=True,
                status_codes=["401"]
            ),
            OpenApiExample(
                "Internal server error",
                description="Internal server error",
                value={"status": "failed"},
                response_only=True,
                status_codes=["500"]
            )
        ],
    )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ChargesBy(generics.GenericAPIView):
    """
        Return the amount each operator owes to the provided op_ID for a given period of time
    """

    serializer_class = PassSerializer_PassesAnalysis
    invalid_request_response = Response({"status": "failed"}, status.HTTP_400_BAD_REQUEST)

    def get_costs_between_operators(self, op1_abbr, op2_abbr, date_from, date_to):
        op1_id = (Provider.objects.get(providerabbr=op1_abbr)).providerid
        op2_id = (Provider.objects.get(providerabbr=op2_abbr)).providerid
        # Find all the vehicles with tags of op2
        op2_vehicles = Vehicle.objects.filter(providerabbr=op2_id)
        # Find all the stations with tags of op1
        op1_stations = Station.objects.filter(stationprovider=op1_id)
        qs = Pass.objects.filter(timestamp__lte=date_to, timestamp__gte=date_from, stationref__in=op1_stations,
                                 vehicleref__in=op2_vehicles)
        price = qs.aggregate(Sum('charge'))['charge__sum']
        serializer = self.get_serializer(qs, many=True)
        data = serializer.data

        if len(data) == 0:
            price = 0
        response_data = {
            'VisitingOperator': op2_abbr,
            'NumberOfPasses': len(data),
            'PassesCost': price
        }
        return response_data

    @extend_schema (
        responses={
            200: inline_serializer(
                name='ChargesBy 200',
                fields= {
                    'op_ID': serializers.CharField(),
                    'RequestTimestamp': serializers.DateTimeField(),
                    'PeriodFrom': serializers.DateField(),
                    'PeriodTo': serializers.DateField(),
                    'PPOList': inline_serializer(
                        name='PPOList',
                        fields={
                        'VisitingOperator': serializers.CharField(),
                        'NumberOfPasses': serializers.IntegerField(),
                        'PassesCost': serializers.FloatField()
                        }
            )
               }
            ),
            400: inline_serializer(
                name='ChargesBy 400',
                fields={
                    'status': serializers.CharField()
                }
            ),
            401: PolymorphicProxySerializer(
                component_name='Status code 401',   
                serializers=[
                    inline_serializer(
                        name="401 No credentials",
                        fields={
                         "detail": serializers.CharField()
                        }
                    ),
                    inline_serializer(
                        name='401 Invalid Token',
                        fields={
                            "detail": serializers.CharField(),
                            "code": serializers.CharField(),
                            "messages": inline_serializer(
                                name="messages",
                                fields={
                                    "token_class": serializers.CharField(),
                                    "token_type": serializers.CharField(),
                                    "message": serializers.CharField()
                                }
                            )
                        }
                    )
                ],
                resource_type_field_name= None,
            ),
            500: inline_serializer(
                name='ChargesBy 500',
                fields={
                    'status': serializers.CharField()
                }
            )
        },
        examples=[
            OpenApiExample(
                "Successful",
                description="An example of a successful endpoint call.",
                value=examples.ourdict["ChargesBy"],
                response_only=True,
                status_codes=["200"],
            ),
            OpenApiExample(
                "Bad request",
                description="An example of a failed endpoint call due to bad request.",
                value={"status": "failed"},
                response_only=True,
                status_codes=["400"],
            ),
            OpenApiExample(
                "No credentials",
                description="Output when credentials are not provided.",
                value=examples.ourdict["Unauthorized_noCredentials"],
                response_only=True,
                status_codes=["401"]
            ),
            OpenApiExample(
                "Invalid Token",
                description="Token is invalid.",
                value=examples.ourdict["Unauthorized_invalidToken"],
                response_only=True,
                status_codes=["401"]
            ),
            OpenApiExample(
                "Internal server error",
                description="Internal server error",
                value={"status": "failed"},
                response_only=True,
                status_codes=["500"]
            )
        ],
    )
    def get(self, request, *args, **kwargs):

        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        op_id_from_request = self.kwargs['op_ID']
        other_operators_ids = Provider.objects.exclude(providerabbr=op_id_from_request)

        date_from = get_datetime_from_kwarg(self.kwargs['datefrom']).date()
        date_to = get_datetime_from_kwarg(self.kwargs['dateto']).date()
        costs = []

        for visiting_operator_id in other_operators_ids:
            visiting_operator_abbr = visiting_operator_id.providerabbr
            try:
                cost = self.get_costs_between_operators(op_id_from_request, visiting_operator_abbr, date_from, date_to)
            except Exception as e:
                return self.invalid_request_response
            costs.append(cost)
        response_data = {
            'op_ID': op_id_from_request,
            'RequestTimestamp': time_now,
            'PeriodFrom': date_from,
            'PeriodTo': date_to,
            'PPOList': costs
        }
        """
        Check if there is no data, then return the same format but with 402 Response code
        Returning the same format instead of eg an empty body is an implementation decision and can be changed if 
        required by simply setting response_data to whatever the response should be
        
        In the current implementation for this particular endpoint there is no way that len(costs) == 0 since we are
        not excluding operators who haven't had any passes in the specified time period
        If this is to change, meaning we are discarding the cost objects where NumberOfPasses == 0 in the costs list
        then this would be possible
        Leaving it here for this exact case it is decided to change in the future and for consistency with the other
        API endpoints 
        """
        if len(costs) == 0:
            response_code = status.HTTP_402_PAYMENT_REQUIRED
        else:
            response_code = status.HTTP_200_OK
        return Response(response_data, status=response_code)
