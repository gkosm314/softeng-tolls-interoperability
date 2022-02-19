from rest_framework import serializers
from backend import models


class PassSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pass
        fields = '__all__'


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Station
        fields = '__all__'

class PassesAnalysisSerializer(serializers.Serializer):
    op1_ID = serializers.CharField()
    op2_ID = serializers.CharField()
    RequestTimestamp = serializers.DateTimeField()
    PeriodFrom = serializers.DateTimeField()
    PeriodTo =  serializers.DateTimeField()
    NumberOfPasses = serializers.IntegerField()
    PassesList = PassSerializer(many=True)
               
