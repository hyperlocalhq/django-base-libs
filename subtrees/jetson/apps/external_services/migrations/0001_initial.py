# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Service'
        db.create_table('external_services_service', south_cleaned_fields((
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sysname', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('api_key', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('user', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
        )))
        db.send_create_signal('external_services', ['Service'])

        # Adding model 'ObjectMapper'
        db.create_table('external_services_objectmapper', south_cleaned_fields((
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['external_services.Service'])),
            ('external_id', self.gf('django.db.models.fields.CharField')(max_length=512)),
        )))
        db.send_create_signal('external_services', ['ObjectMapper'])

        # Adding model 'ServiceActionLog'
        db.create_table('external_services_serviceactionlog', south_cleaned_fields((
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['external_services.Service'])),
            ('request', self.gf('base_libs.models.fields.PlainTextModelField')(blank=True)),
            ('response', self.gf('base_libs.models.fields.PlainTextModelField')(blank=True)),
            ('response_code', self.gf('django.db.models.fields.IntegerField')(blank=True)),
        )))
        db.send_create_signal('external_services', ['ServiceActionLog'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Service'
        db.delete_table('external_services_service')

        # Deleting model 'ObjectMapper'
        db.delete_table('external_services_objectmapper')

        # Deleting model 'ServiceActionLog'
        db.delete_table('external_services_serviceactionlog')
    
    
    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('app_label', 'name')", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'external_services.objectmapper': {
            'Meta': {'ordering': "('external_id',)", 'object_name': 'ObjectMapper'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['external_services.Service']"})
        },
        'external_services.service': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Service'},
            'api_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'sysname': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'})
        },
        'external_services.serviceactionlog': {
            'Meta': {'ordering': "('-creation_date',)", 'object_name': 'ServiceActionLog'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'request': ('base_libs.models.fields.PlainTextModelField', [], {'blank': 'True'}),
            'response': ('base_libs.models.fields.PlainTextModelField', [], {'blank': 'True'}),
            'response_code': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['external_services.Service']"})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['external_services']
