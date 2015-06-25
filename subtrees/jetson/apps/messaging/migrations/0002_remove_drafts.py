# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from jetson.apps.messaging.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    no_dry_run = True
    depends_on = (
        ("navigation", "0001_initial"),
    )
    
    def forwards(self, orm):
        NavigationLink = models.get_model("navigation", "NavigationLink")
        NavigationLink.objects.filter(
            parent__sysname="messages",
            sysname="drafts",
            ).delete()
    
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
