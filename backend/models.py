# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Pass(models.Model):
    passid = models.CharField(db_column='passID', primary_key=True, max_length=10)
    timestamp = models.DateTimeField()
    stationref = models.ForeignKey('Station', models.DO_NOTHING, db_column='stationRef')
    vehicleref = models.ForeignKey('Vehicle', models.DO_NOTHING, db_column='vehicleRef')
    charge = models.FloatField()
    providerabbr = models.ForeignKey('Provider', models.DO_NOTHING, db_column='providerAbbr')
    ishome = models.IntegerField(db_column='isHome')

    class Meta:
        db_table = 'Passes'


class Payment(models.Model):
    transactionid = models.AutoField(db_column='transactionID', primary_key=True)
    providercreditedid = models.ForeignKey('Provider', models.DO_NOTHING, db_column='providerCreditedID', related_name = 'provider_credited_id')  
    providerdebitedid = models.ForeignKey('Provider', models.DO_NOTHING, db_column='providerDebitedID', related_name = 'provider_debited_id')  
    amount = models.IntegerField()
    status = models.CharField(max_length=10)

    class Meta:
        db_table = 'Payments'


class Provider(models.Model):
    providerid = models.AutoField(db_column='providerID', primary_key=True)
    providername = models.CharField(db_column='providerName', unique=True, max_length=20)
    providerabbr = models.CharField(db_column='providerAbbr', unique=True, max_length=2)
    isvalid = models.IntegerField(db_column='isValid')

    class Meta:
        db_table = 'Providers'


class Station(models.Model):
    stationid = models.CharField(db_column='stationID', primary_key=True, max_length=10)
    stationprovider = models.ForeignKey(Provider, models.DO_NOTHING, db_column='stationProvider')
    stationname = models.CharField(db_column='stationName', unique=True, max_length=30)
    isvalid = models.IntegerField(db_column='isValid')

    class Meta:
        db_table = 'Stations'


class Vehicle(models.Model):
    vehicleid = models.CharField(db_column='vehicleID', primary_key=True, max_length=12)
    tagid = models.CharField(db_column='tagID', max_length=9)
    tagprovider = models.CharField(db_column='tagProvider', max_length=20)
    providerabbr = models.ForeignKey(Provider, models.DO_NOTHING, db_column='providerAbbr')
    licenseyear = models.IntegerField(db_column='licenseYear')
    isvalid = models.IntegerField(db_column='isValid')

    class Meta:
        db_table = 'Vehicles'
