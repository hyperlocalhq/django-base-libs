# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Changing field 'HttpState.httpstate_key'
        db.alter_column(u'httpstate_httpstate', 'httpstate_key', self.gf('django.db.models.fields.CharField')(max_length=40, primary_key=True))

        # Changing field 'HttpState.httpstate_data'
        db.alter_column(u'httpstate_httpstate', 'httpstate_data', self.gf('django.db.models.fields.TextField')())

        # Changing field 'HttpState.expire_date'
        db.alter_column(u'httpstate_httpstate', 'expire_date', self.gf('django.db.models.fields.DateTimeField')())
    
    
    def backwards(self, orm):
        
        # Changing field 'HttpState.httpstate_key'
        db.alter_column(u'httpstate_httpstate', 'httpstate_key', self.gf('models.CharField')(_('httpstate key'), max_length=40, primary_key=True))

        # Changing field 'HttpState.httpstate_data'
        db.alter_column(u'httpstate_httpstate', 'httpstate_data', self.gf('models.TextField')(_('httpstate data')))

        # Changing field 'HttpState.expire_date'
        db.alter_column(u'httpstate_httpstate', 'expire_date', self.gf('models.DateTimeField')(_('expire date')))
    
    
    models = {
        u'httpstate.httpstate': {
            'Meta': {'object_name': 'HttpState'},
            'expire_date': ('django.db.models.fields.DateTimeField', [], {}),
            'httpstate_data': ('django.db.models.fields.TextField', [], {}),
            'httpstate_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['httpstate']
