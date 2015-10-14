# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(DataMigration):
    
    def forwards(self, orm):
        from django.core.management import call_command
        call_command("loaddata", "default_i18n_data.json")
    
    def backwards(self, orm):
        pass
    
    models = {
        'i18n.area': {
            'Meta': {'ordering': "['country']", 'unique_together': "(('country', 'name'),)", 'object_name': 'Area'},
            'abbrev': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'alt_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['i18n.Country']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name_id': ('django.db.models.fields.CharField', [], {'max_length': '6', 'primary_key': 'True'}),
            'reg_area': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'})
        },
        'i18n.country': {
            'Meta': {'object_name': 'Country'},
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
        'i18n.countrylanguage': {
            'Meta': {'ordering': "['country']", 'object_name': 'CountryLanguage'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['i18n.Country']"}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '6', 'primary_key': 'True'}),
            'lang_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['i18n.Language']"})
        },
        'i18n.language': {
            'Meta': {'object_name': 'Language'},
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso2_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'iso3_code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'name_de': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'sort_order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '20'}),
            'synonym': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'})
        },
        'i18n.nationality': {
            'Meta': {'object_name': 'Nationality'},
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'name_de': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'sort_order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '20'})
        },
        'i18n.phone': {
            'Meta': {'ordering': "['country']", 'object_name': 'Phone'},
            'code': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['i18n.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'int_prefix': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'ln_area': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'ln_area_sn': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'ln_sn': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'nat_prefix': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'})
        },
        'i18n.timezone': {
            'Meta': {'ordering': "['zone']", 'object_name': 'TimeZone'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['i18n.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'zone': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['i18n']
