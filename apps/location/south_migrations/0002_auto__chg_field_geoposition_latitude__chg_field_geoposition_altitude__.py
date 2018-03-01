# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Changing field 'Geoposition.latitude'
        db.alter_column(u'location_geoposition', 'latitude', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'Geoposition.altitude'
        db.alter_column(u'location_geoposition', 'altitude', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Geoposition.longitude'
        db.alter_column(u'location_geoposition', 'longitude', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'Geoposition.address'
        db.alter_column(u'location_geoposition', 'address_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['location.Address']))

        # Changing field 'Address.city'
        db.alter_column(u'location_address', 'city', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Address.country'
        db.alter_column(u'location_address', 'country_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['i18n.Country'], null=True))

        # Changing field 'Address.street_address3'
        db.alter_column(u'location_address', 'street_address3', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Address.street_address2'
        db.alter_column(u'location_address', 'street_address2', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Address.state'
        db.alter_column(u'location_address', 'state', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Address.postal_code'
        db.alter_column(u'location_address', 'postal_code', self.gf('django.db.models.fields.CharField')(max_length=10))

        # Changing field 'Address.street_address'
        db.alter_column(u'location_address', 'street_address', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Locality.neighborhood'
        db.alter_column(u'location_locality', 'neighborhood', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Locality.district'
        db.alter_column(u'location_locality', 'district', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Locality.address'
        db.alter_column(u'location_locality', 'address_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['location.Address']))
    
    
    def backwards(self, orm):
        
        # Changing field 'Geoposition.latitude'
        db.alter_column(u'location_geoposition', 'latitude', self.gf('models.FloatField')(_("Latitude"), null=True))

        # Changing field 'Geoposition.altitude'
        db.alter_column(u'location_geoposition', 'altitude', self.gf('models.IntegerField')(_("Altitude"), null=True))

        # Changing field 'Geoposition.longitude'
        db.alter_column(u'location_geoposition', 'longitude', self.gf('models.FloatField')(_("Longitude"), null=True))

        # Changing field 'Geoposition.address'
        db.alter_column(u'location_geoposition', 'address_id', self.gf('models.ForeignKey')(orm['location.Address']))

        # Changing field 'Address.city'
        db.alter_column(u'location_address', 'city', self.gf('models.CharField')(_("City"), max_length=255))

        # Changing field 'Address.country'
        db.alter_column(u'location_address', 'country_id', self.gf('models.ForeignKey')(orm['i18n.Country'], null=True))

        # Changing field 'Address.street_address3'
        db.alter_column(u'location_address', 'street_address3', self.gf('models.CharField')(_("Additional Address"), max_length=255))

        # Changing field 'Address.street_address2'
        db.alter_column(u'location_address', 'street_address2', self.gf('models.CharField')(_("Additional Address"), max_length=255))

        # Changing field 'Address.state'
        db.alter_column(u'location_address', 'state', self.gf('models.CharField')(_("State"), max_length=255))

        # Changing field 'Address.postal_code'
        db.alter_column(u'location_address', 'postal_code', self.gf('models.CharField')(_("Postal/ZIP Code"), max_length=10))

        # Changing field 'Address.street_address'
        db.alter_column(u'location_address', 'street_address', self.gf('models.CharField')(_("Street Address"), max_length=255))

        # Changing field 'Locality.neighborhood'
        db.alter_column(u'location_locality', 'neighborhood', self.gf('models.CharField')(_("Neighborhood"), max_length=255))

        # Changing field 'Locality.district'
        db.alter_column(u'location_locality', 'district', self.gf('models.CharField')(_("District"), max_length=255))

        # Changing field 'Locality.address'
        db.alter_column(u'location_locality', 'address_id', self.gf('models.ForeignKey')(orm['location.Address']))
    
    
    models = {
        u'i18n.country': {
            'Meta': {'ordering': "['sort_order', 'name']", 'object_name': 'Country'},
            'adm_area': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'iso2_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2', 'primary_key': 'True'}),
            'iso3_code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '56'}),
            'name_de': ('django.db.models.fields.CharField', [], {'max_length': '56', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'sort_order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '20'}),
            'territory_of': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'})
        },
        u'location.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'default': "'DE'", 'to': u"orm['i18n.Country']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'street_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'street_address2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'street_address3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'location.geoposition': {
            'Meta': {'object_name': 'Geoposition'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['location.Address']"}),
            'altitude': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'location.locality': {
            'Meta': {'object_name': 'Locality'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['location.Address']"}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'neighborhood': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['location']
