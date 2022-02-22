from rest_framework import serializers
from backend import models


class PassSerializer_PassesPerStation(serializers.ModelSerializer):
    """
    A custom serializer for the Pass model, to be used on the PassesPerStation API endpoint
    Changing field names and transforming some values
    """

    PassIndex = serializers.SerializerMethodField()
    PassID = serializers.CharField(source='passid')
    PassTimeStamp = serializers.DateTimeField(source='timestamp')
    VehicleID = serializers.CharField(source='vehicleref')
    TagProvider = serializers.CharField(source='stationref.stationprovider.providerabbr')
    PassType = serializers.CharField(source='is_home_str')
    PassCharge = serializers.CharField(source='charge')
    pass_index = 0

    def get_PassIndex(self, obj)->int:
        self.pass_index += 1
        return self.pass_index

    class Meta:
        model = models.Pass
        fields = ('PassIndex', 'PassID', 'PassTimeStamp', 'VehicleID', 'TagProvider', 'PassType', 'PassCharge')


class PassSerializer_PassesAnalysis(serializers.ModelSerializer):
    """
    A custom serializer for the Pass model, to be used on the PassesPerStation API endpoint
    Changing field names and transforming some values
    """

    PassIndex = serializers.SerializerMethodField()
    PassID = serializers.CharField(source='passid')
    StationID = serializers.CharField(source='stationref')
    TimeStamp = serializers.DateTimeField(source='timestamp')
    VehicleID = serializers.CharField(source='vehicleref')
    Charge = serializers.CharField(source='charge')
    pass_index = 0

    def get_PassIndex(self, obj)->int:
        self.pass_index += 1
        return self.pass_index

    class Meta:
        model = models.Pass
        fields = ('PassIndex', 'PassID', 'StationID', 'TimeStamp', 'VehicleID', 'Charge')


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Station
        fields = '__all__'
               
