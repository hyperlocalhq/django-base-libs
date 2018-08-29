# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Geolocation(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True, editable=False)
    country = models.CharField(max_length=6, db_column='Country')
    language = models.CharField(max_length=6, db_column='Language')
    iso2 = models.CharField(max_length=18, db_column='ISO2')
    region1 = models.CharField(max_length=180, db_column='Region1', blank=True)
    region2 = models.CharField(max_length=180, db_column='Region2', blank=True)
    region3 = models.CharField(max_length=180, db_column='Region3', blank=True)
    region4 = models.CharField(max_length=180, db_column='Region4', blank=True)
    zip_code = models.CharField(max_length=30, db_column='ZIP')
    city = models.CharField(max_length=180, db_column='City', blank=True)
    area1 = models.CharField(max_length=240, db_column='Area1', blank=True)
    area2 = models.CharField(max_length=240, db_column='Area2', blank=True)
    lat = models.FloatField(db_column='Lat')
    lng = models.FloatField(db_column='Lng')
    tz = models.CharField(max_length=90, db_column='TZ')
    utc = models.CharField(max_length=30, db_column='UTC')
    dst = models.CharField(max_length=3, db_column='DST')
    
    class Meta:
        verbose_name = _("geolocation")
        verbose_name_plural = _("geolocations")
        db_table = u'GeoPC'
        
    def __unicode__(self):
        return self.region3
