# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from jetson.apps.history.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'ExtendedLogEntry'
        db.create_table('history_extendedlogentry', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('content_type', models.ForeignKey(orm['contenttypes.ContentType'], limit_choices_to={}, related_name=None, null=True, blank=True)),
            ('object_id', models.CharField(u'Related object', max_length=255, null=False, blank=True)),
            ('action_time', models.DateTimeField(_('action time'), auto_now=True)),
            ('user', models.ForeignKey(orm['auth.User'])),
            ('object_repr', models.CharField(_('object repr'), max_length=200)),
            ('action_flag', models.PositiveSmallIntegerField(_('action'), default=0)),
            ('change_message', models.TextField(_('change message'), blank=True)),
            ('change_message_de', models.TextField(_('change message'), blank=True)),
            ('scope', models.PositiveSmallIntegerField(_('scope'), default=0)),
        )))
        db.send_create_signal('history', ['ExtendedLogEntry'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'ExtendedLogEntry'
        db.delete_table('history_extendedlogentry')
        
    
    
    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'history.extendedlogentry': {
            'Meta': {'ordering': "('-action_time',)"},
            'action_flag': ('models.PositiveSmallIntegerField', ["_('action')"], {'default': '0'}),
            'action_time': ('models.DateTimeField', ["_('action time')"], {'auto_now': 'True'}),
            'change_message': ('models.TextField', ["_('change message')"], {'blank': 'True'}),
            'change_message_de': ('models.TextField', ["_('change message')"], {'blank': 'True'}),
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'limit_choices_to': '{}', 'related_name': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('models.CharField', ["u'Related object'"], {'max_length': '255', 'null': 'False', 'blank': 'True'}),
            'object_repr': ('models.CharField', ["_('object repr')"], {'max_length': '200'}),
            'scope': ('models.PositiveSmallIntegerField', ["_('scope')"], {'default': '0'}),
            'user': ('models.ForeignKey', ["orm['auth.User']"], {})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['history']
