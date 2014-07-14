
from south.db import db
from django.db import models
from ccb.apps.external_services.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Service'
        db.create_table('external_services_service', south_cleaned_fields((
            ('id', orm['external_services.Service:id']),
            ('sysname', orm['external_services.Service:sysname']),
            ('title', orm['external_services.Service:title']),
            ('url', orm['external_services.Service:url']),
            ('api_key', orm['external_services.Service:api_key']),
            ('user', orm['external_services.Service:user']),
            ('password', orm['external_services.Service:password']),
        )))
        db.send_create_signal('external_services', ['Service'])
        
        # Adding model 'ObjectMapper'
        db.create_table('external_services_objectmapper', south_cleaned_fields((
            ('id', orm['external_services.ObjectMapper:id']),
            ('content_type', orm['external_services.ObjectMapper:content_type']),
            ('object_id', orm['external_services.ObjectMapper:object_id']),
            ('service', orm['external_services.ObjectMapper:service']),
            ('external_id', orm['external_services.ObjectMapper:external_id']),
        )))
        db.send_create_signal('external_services', ['ObjectMapper'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Service'
        db.delete_table('external_services_service')
        
        # Deleting model 'ObjectMapper'
        db.delete_table('external_services_objectmapper')
        
    
    
    models = {
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'external_services.objectmapper': {
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'related_name': 'None', 'null': 'False', 'blank': 'False'}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('models.CharField', ["u'Related object'"], {'max_length': '255', 'null': 'False', 'blank': 'False'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['external_services.Service']"})
        },
        'external_services.service': {
            'api_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'sysname': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['external_services']
