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
