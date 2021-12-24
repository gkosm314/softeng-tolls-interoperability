# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Passes(models.Model):
    passid = models.CharField(db_column='passID', primary_key=True, max_length=10)  # Field name made lowercase.
    timestamp = models.DateTimeField()
    stationref = models.ForeignKey('Stations', models.DO_NOTHING, db_column='stationRef')  # Field name made lowercase.
    vehicleref = models.ForeignKey('Vehicles', models.DO_NOTHING, db_column='vehicleRef')  # Field name made lowercase.
    charge = models.FloatField()
    providerabbr = models.ForeignKey('Providers', models.DO_NOTHING, db_column='providerAbbr')  # Field name made lowercase.
    ishome = models.IntegerField(db_column='isHome')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Passes'


class Payments(models.Model):
    transactionid = models.AutoField(db_column='transactionID', primary_key=True)  # Field name made lowercase.
    providercreditedid = models.ForeignKey('Providers', models.DO_NOTHING, db_column='providerCreditedID')  # Field name made lowercase.
    providerdebitedid = models.ForeignKey('Providers', models.DO_NOTHING, db_column='providerDebitedID')  # Field name made lowercase.
    amount = models.IntegerField()
    status = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'Payments'


class Providers(models.Model):
    providerid = models.AutoField(db_column='providerID', primary_key=True)  # Field name made lowercase.
    providername = models.CharField(db_column='providerName', unique=True, max_length=20)  # Field name made lowercase.
    providerabbr = models.CharField(db_column='providerAbbr', unique=True, max_length=2)  # Field name made lowercase.
    isvalid = models.IntegerField(db_column='isValid')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Providers'


class Stations(models.Model):
    stationid = models.CharField(db_column='stationID', primary_key=True, max_length=10)  # Field name made lowercase.
    stationprovider = models.ForeignKey(Providers, models.DO_NOTHING, db_column='stationProvider')  # Field name made lowercase.
    stationname = models.CharField(db_column='stationName', unique=True, max_length=30)  # Field name made lowercase.
    isvalid = models.IntegerField(db_column='isValid')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Stations'


class Vehicles(models.Model):
    vehicleid = models.CharField(db_column='vehicleID', primary_key=True, max_length=12)  # Field name made lowercase.
    tagid = models.CharField(db_column='tagID', max_length=9)  # Field name made lowercase.
    tagprovider = models.CharField(db_column='tagProvider', max_length=20)  # Field name made lowercase.
    providerabbr = models.ForeignKey(Providers, models.DO_NOTHING, db_column='providerAbbr')  # Field name made lowercase.
    licenseyear = models.IntegerField(db_column='licenseYear')  # Field name made lowercase.
    isvalid = models.IntegerField(db_column='isValid')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Vehicles'
