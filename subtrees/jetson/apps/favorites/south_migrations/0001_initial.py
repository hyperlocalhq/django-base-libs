# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from jetson.apps.favorites.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Favorite'
        db.create_table('favorites_favorite', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('content_type', models.ForeignKey(orm['contenttypes.ContentType'], limit_choices_to={}, related_name=None, null=False, blank=False)),
            ('object_id', models.CharField(u'Related object', max_length=255, null=False, blank=False)),
            ('user', models.ForeignKey(orm['auth.User'])),
        )))
        db.send_create_signal('favorites', ['Favorite'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Favorite'
        db.delete_table('favorites_favorite')
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'favorites.favorite': {
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'limit_choices_to': '{}', 'related_name': 'None', 'null': 'False', 'blank': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('models.CharField', ["u'Related object'"], {'max_length': '255', 'null': 'False', 'blank': 'False'}),
            'user': ('models.ForeignKey', ["orm['auth.User']"], {})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['favorites']
