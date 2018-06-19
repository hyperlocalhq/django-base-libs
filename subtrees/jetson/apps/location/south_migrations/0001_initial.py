# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from jetson.apps.location.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Geoposition'
        db.create_table('location_geoposition', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('address', models.ForeignKey(orm.Address)),
            ('latitude', models.FloatField(_("Latitude"), null=True, blank=True)),
            ('longitude', models.FloatField(_("Longitude"), null=True, blank=True)),
            ('altitude', models.IntegerField(_("Altitude"), null=True, blank=True)),
        )))
        db.send_create_signal('location', ['Geoposition'])
        
        # Adding model 'Address'
        db.create_table('location_address', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('country', models.ForeignKey(orm['i18n.Country'], default='DE', null=True, blank=True)),
            ('state', models.CharField(_("State"), max_length=255, blank=True)),
            ('city', models.CharField(_("City"), default='Berlin', max_length=255, blank=True)),
            ('street_address', models.CharField(_("Street Address"), max_length=255, blank=True)),
            ('street_address2', models.CharField(_("Additional Address"), max_length=255, blank=True)),
            ('street_address3', models.CharField(_("Additional Address"), max_length=255, blank=True)),
            ('postal_code', models.CharField(_("Postal/ZIP Code"), max_length=10, blank=True)),
        )))
        db.send_create_signal('location', ['Address'])
        
        # Adding model 'Locality'
        db.create_table('location_locality', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('address', models.ForeignKey(orm.Address)),
            ('district', models.CharField(_("District"), max_length=255, blank=True)),
            ('neighborhood', models.CharField(_("Neighborhood"), max_length=255, blank=True)),
        )))
        db.send_create_signal('location', ['Locality'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Geoposition'
        db.delete_table('location_geoposition')
        
        # Deleting model 'Address'
        db.delete_table('location_address')
        
        # Deleting model 'Locality'
        db.delete_table('location_locality')
        
    
    
    models = {
        'i18n.country': {
            'Meta': {'ordering': "['sort_order','name']"},
            '_stub': True,
            'iso2_code': ('models.CharField', ["_('Alpha-2 ISO Code')"], {'unique': 'True', 'max_length': '2', 'primary_key': 'True'})
        },
        'location.geoposition': {
            'address': ('models.ForeignKey', ["orm['location.Address']"], {}),
            'altitude': ('models.IntegerField', ['_("Altitude")'], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('models.FloatField', ['_("Latitude")'], {'null': 'True', 'blank': 'True'}),
            'longitude': ('models.FloatField', ['_("Longitude")'], {'null': 'True', 'blank': 'True'})
        },
        'location.address': {
            'city': ('models.CharField', ['_("City")'], {'default': "'Berlin'", 'max_length': '255', 'blank': 'True'}),
            'country': ('models.ForeignKey', ["orm['i18n.Country']"], {'default': "'DE'", 'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'postal_code': ('models.CharField', ['_("Postal/ZIP Code")'], {'max_length': '10', 'blank': 'True'}),
            'state': ('models.CharField', ['_("State")'], {'max_length': '255', 'blank': 'True'}),
            'street_address': ('models.CharField', ['_("Street Address")'], {'max_length': '255', 'blank': 'True'}),
            'street_address2': ('models.CharField', ['_("Additional Address")'], {'max_length': '255', 'blank': 'True'}),
            'street_address3': ('models.CharField', ['_("Additional Address")'], {'max_length': '255', 'blank': 'True'})
        },
        'location.locality': {
            'address': ('models.ForeignKey', ["orm['location.Address']"], {}),
            'district': ('models.CharField', ['_("District")'], {'max_length': '255', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'neighborhood': ('models.CharField', ['_("Neighborhood")'], {'max_length': '255', 'blank': 'True'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['location']
