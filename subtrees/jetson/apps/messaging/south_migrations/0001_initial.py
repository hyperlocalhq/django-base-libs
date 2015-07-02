# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from jetson.apps.messaging.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'InternalMessage'
        db.create_table('messaging_internalmessage', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('creation_date', models.DateTimeField(_("creation date"), editable=False)),
            ('modified_date', models.DateTimeField(_("modified date"), null=True, editable=False)),
            ('creator', models.ForeignKey(orm['auth.User'], editable=False, related_name="%(class)s_creator", null=True)),
            ('modifier', models.ForeignKey(orm['auth.User'], editable=False, related_name="%(class)s_modifier", null=True)),
            ('sender', models.ForeignKey(orm['auth.User'], related_name="sent_message_set", null=True, blank=True)),
            ('recipient', models.ForeignKey(orm['auth.User'], related_name="received_message_set", null=True, blank=True)),
            ('subject', models.CharField(_("Subject"), max_length=255, blank=True)),
            ('body', ExtendedTextField(_("Message"), blank=True)),
            ('is_read', models.BooleanField(_("Read"), default=False)),
            ('is_deleted', models.BooleanField(_("Deleted"), default=False)),
            ('is_replied', models.BooleanField(_("Replied"), default=False)),
            ('is_spam', models.BooleanField(_("Spam"), default=False)),
            ('is_draft', models.BooleanField(_("Draft"), default=False)),
            ('body_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
        )))
        db.send_create_signal('messaging', ['InternalMessage'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'InternalMessage'
        db.delete_table('messaging_internalmessage')
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'messaging.internalmessage': {
            'Meta': {'ordering': "('-cretion_date','subject',)"},
            'body': ('ExtendedTextField', ['_("Message")'], {'blank': 'True'}),
            'body_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'editable': 'False'}),
            'creator': ('models.ForeignKey', ["orm['auth.User']"], {'editable': 'False', 'related_name': '"%(class)s_creator"', 'null': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'is_deleted': ('models.BooleanField', ['_("Deleted")'], {'default': 'False'}),
            'is_draft': ('models.BooleanField', ['_("Draft")'], {'default': 'False'}),
            'is_read': ('models.BooleanField', ['_("Read")'], {'default': 'False'}),
            'is_replied': ('models.BooleanField', ['_("Replied")'], {'default': 'False'}),
            'is_spam': ('models.BooleanField', ['_("Spam")'], {'default': 'False'}),
            'modified_date': ('models.DateTimeField', ['_("modified date")'], {'null': 'True', 'editable': 'False'}),
            'modifier': ('models.ForeignKey', ["orm['auth.User']"], {'editable': 'False', 'related_name': '"%(class)s_modifier"', 'null': 'True'}),
            'recipient': ('models.ForeignKey', ["orm['auth.User']"], {'related_name': '"received_message_set"', 'null': 'True', 'blank': 'True'}),
            'sender': ('models.ForeignKey', ["orm['auth.User']"], {'related_name': '"sent_message_set"', 'null': 'True', 'blank': 'True'}),
            'subject': ('models.CharField', ['_("Subject")'], {'max_length': '255', 'blank': 'True'}),
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['messaging']
