# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from jetson.apps.profanity_filter.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'SwearingCase'
        db.create_table('profanity_filter_swearingcase', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('creation_date', models.DateTimeField(_("creation date"), editable=False)),
            ('content_type', models.ForeignKey(orm['contenttypes.ContentType'], related_name=None, null=True, blank=True)),
            ('object_id', models.CharField(u'Related object', max_length=255, null=False, blank=True)),
            ('user', models.ForeignKey(orm['auth.User'], null=True, blank=True)),
            ('used_words', models.TextField(_("used words"))),
        )))
        db.send_create_signal('profanity_filter', ['SwearingCase'])
        
        # Adding model 'SwearWord'
        db.create_table('profanity_filter_swearword', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('word', models.CharField(_("Word to filter out"), max_length=80)),
        )))
        db.send_create_signal('profanity_filter', ['SwearWord'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'SwearingCase'
        db.delete_table('profanity_filter_swearingcase')
        
        # Deleting model 'SwearWord'
        db.delete_table('profanity_filter_swearword')
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'profanity_filter.swearingcase': {
            'Meta': {'ordering': "('-creation_date',)"},
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'related_name': 'None', 'null': 'True', 'blank': 'True'}),
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'editable': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('models.CharField', ["u'Related object'"], {'max_length': '255', 'null': 'False', 'blank': 'True'}),
            'used_words': ('models.TextField', ['_("used words")'], {}),
            'user': ('models.ForeignKey', ["orm['auth.User']"], {'null': 'True', 'blank': 'True'})
        },
        'profanity_filter.swearword': {
            'Meta': {'ordering': "('word',)"},
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'word': ('models.CharField', ['_("Word to filter out")'], {'max_length': '80'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['profanity_filter']
