
from south.db import db
from django.db import models
from jetson.apps.httpstate.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'HttpState'
        db.create_table('httpstate_httpstate', south_cleaned_fields((
            ('httpstate_key', models.CharField(_('httpstate key'), max_length=40, primary_key=True)),
            ('httpstate_data', models.TextField(_('httpstate data'))),
            ('expire_date', models.DateTimeField(_('expire date'))),
        )))
        db.send_create_signal('httpstate', ['HttpState'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'HttpState'
        db.delete_table('httpstate_httpstate')
        
    
    
    models = {
        'httpstate.httpstate': {
            'expire_date': ('models.DateTimeField', ["_('expire date')"], {}),
            'httpstate_data': ('models.TextField', ["_('httpstate data')"], {}),
            'httpstate_key': ('models.CharField', ["_('httpstate key')"], {'max_length': '40', 'primary_key': 'True'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['httpstate']
