# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Pass(models.Model):
    passid = models.CharField(db_column='passID', primary_key=True, max_length=10)  # Field name made lowercase.
    timestamp = models.DateTimeField()
    stationref = models.ForeignKey('Station', models.DO_NOTHING, db_column='stationRef')  # Field name made lowercase.
    vehicleref = models.ForeignKey('Vehicle', models.DO_NOTHING, db_column='vehicleRef')  # Field name made lowercase.
    charge = models.FloatField()
    providerabbr = models.ForeignKey('Provider', models.DO_NOTHING, db_column='providerAbbr')  # Field name made lowercase.
    ishome = models.IntegerField(db_column='isHome')  # Field name made lowercase.

    class Meta:
        db_table = 'Passes'


class Payment(models.Model):
    transactionid = models.AutoField(db_column='transactionID', primary_key=True)  # Field name made lowercase.
    providercreditedid = models.ForeignKey('Provider', models.DO_NOTHING, db_column='providerCreditedID', related_name = 'provider_credited_id')  # Field name made lowercase.  
    providerdebitedid = models.ForeignKey('Provider', models.DO_NOTHING, db_column='providerDebitedID', related_name = 'provider_debited_id')  # Field name made lowercase.  
    amount = models.IntegerField()
    status = models.CharField(max_length=10)

    class Meta:
        db_table = 'Payments'


class Provider(models.Model):
    providerid = models.AutoField(db_column='providerID', primary_key=True)  # Field name made lowercase.
    providername = models.CharField(db_column='providerName', unique=True, max_length=20)  # Field name made lowercase.
    providerabbr = models.CharField(db_column='providerAbbr', unique=True, max_length=2)  # Field name made lowercase.
    isvalid = models.IntegerField(db_column='isValid')  # Field name made lowercase.

    class Meta:
        db_table = 'Providers'


class Station(models.Model):
    stationid = models.CharField(db_column='stationID', primary_key=True, max_length=10)  # Field name made lowercase.
    stationprovider = models.ForeignKey(Provider, models.DO_NOTHING, db_column='stationProvider')  # Field name made lowercase.
    stationname = models.CharField(db_column='stationName', unique=True, max_length=30)  # Field name made lowercase.
    isvalid = models.IntegerField(db_column='isValid')  # Field name made lowercase.

    class Meta:
        db_table = 'Stations'


class Vehicle(models.Model):
    vehicleid = models.CharField(db_column='vehicleID', primary_key=True, max_length=12)  # Field name made lowercase.
    tagid = models.CharField(db_column='tagID', max_length=9)  # Field name made lowercase.
    tagprovider = models.CharField(db_column='tagProvider', max_length=20)  # Field name made lowercase.
    providerabbr = models.ForeignKey(Provider, models.DO_NOTHING, db_column='providerAbbr')  # Field name made lowercase.
    licenseyear = models.IntegerField(db_column='licenseYear')  # Field name made lowercase.
    isvalid = models.IntegerField(db_column='isValid')  # Field name made lowercase.

    class Meta:
        db_table = 'Vehicles'
