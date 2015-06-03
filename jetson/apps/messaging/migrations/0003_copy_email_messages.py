# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from jetson.apps.messaging.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    no_dry_run = True
    depends_on = (
        ("mailing", "0001_initial"),
    )
    
    def forwards(self, orm):
        from django.db import connection, transaction
        cursor = connection.cursor()
        
        cursor.execute(
            'INSERT INTO messaging_internalmessage '
            '(sender_id, recipient_id, subject, body, body_markup_type,'
            'is_deleted, is_draft, is_read, is_replied, is_spam, creation_date)'
            ' SELECT sender_id, recipient_id, subject, body_html,'
            ' body_html_markup_type, is_deleted, is_draft, is_read, is_replied,'
            'is_spam, timestamp FROM mailing_emailmessage '
            'WHERE sender_id IS NOT NULL AND recipient_id IS NOT NULL'
            )
            
        cursor.execute("DELETE FROM mailing_emailmessage WHERE is_internal=1")

    def backwards(self, orm):
        pass
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'messaging.internalmessage': {
            'Meta': {'ordering': "('-creation_date','subject',)"},
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
            'subject': ('models.CharField', ['_("Subject")'], {'max_length': '255', 'blank': 'True'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['messaging']
