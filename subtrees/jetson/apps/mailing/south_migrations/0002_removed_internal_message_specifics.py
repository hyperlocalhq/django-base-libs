# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from jetson.apps.mailing.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields
from base_libs.utils.misc import is_installed

class Migration:

    depends_on = []
    if is_installed("messaging.models"):
        depends_on.append(("messaging", "0003_copy_email_messages"))
    
    def forwards(self, orm):
        from datetime import datetime
        
        # Adding field 'EmailMessage.modifier'
        db.add_column('mailing_emailmessage', 'modifier', models.ForeignKey(orm['auth.User'], editable=False, related_name="%(class)s_modifier", null=True))
        
        # Adding field 'EmailMessage.creation_date'
        db.add_column('mailing_emailmessage', 'creation_date', models.DateTimeField(_("creation date"), editable=False, default=datetime.now))
        
        # Adding field 'EmailMessage.modified_date'
        db.add_column('mailing_emailmessage', 'modified_date', models.DateTimeField(_("modified date"), null=True, editable=False))
        
        # Adding field 'EmailMessage.creator'
        db.add_column('mailing_emailmessage', 'creator', models.ForeignKey(orm['auth.User'], editable=False, related_name="%(class)s_creator", null=True))
        
        # Deleting field 'EmailMessage.is_replied'
        db.delete_column('mailing_emailmessage', 'is_replied')
        
        # Deleting field 'EmailMessage.slug'
        db.delete_column('mailing_emailmessage', 'slug')
        
        # Deleting field 'EmailMessage.is_internal'
        db.delete_column('mailing_emailmessage', 'is_internal')
        
        # Deleting field 'EmailMessage.is_draft'
        db.delete_column('mailing_emailmessage', 'is_draft')
        
        # Deleting field 'EmailMessage.is_spam'
        db.delete_column('mailing_emailmessage', 'is_spam')
        
        # Deleting field 'EmailMessage.is_read'
        db.delete_column('mailing_emailmessage', 'is_read')
        
        # Deleting field 'EmailMessage.is_deleted'
        db.delete_column('mailing_emailmessage', 'is_deleted')
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'EmailMessage.modifier'
        db.delete_column('mailing_emailmessage', 'modifier_id')
        
        # Deleting field 'EmailMessage.creation_date'
        db.delete_column('mailing_emailmessage', 'creation_date')
        
        # Deleting field 'EmailMessage.modified_date'
        db.delete_column('mailing_emailmessage', 'modified_date')
        
        # Deleting field 'EmailMessage.creator'
        db.delete_column('mailing_emailmessage', 'creator_id')
        
        # Adding field 'EmailMessage.is_replied'
        db.add_column('mailing_emailmessage', 'is_replied', models.BooleanField(_("Replied"), default=False))
        
        # Adding field 'EmailMessage.slug'
        db.add_column('mailing_emailmessage', 'slug', models.SlugField(max_length=255, unique=True))
        
        # Adding field 'EmailMessage.is_internal'
        db.add_column('mailing_emailmessage', 'is_internal', models.BooleanField(_("Internal"), default=False))
        
        # Adding field 'EmailMessage.is_draft'
        db.add_column('mailing_emailmessage', 'is_draft', models.BooleanField(_("Draft"), default=False))
        
        # Adding field 'EmailMessage.is_spam'
        db.add_column('mailing_emailmessage', 'is_spam', models.BooleanField(_("Spam"), default=False))
        
        # Adding field 'EmailMessage.is_read'
        db.add_column('mailing_emailmessage', 'is_read', models.BooleanField(_("Read"), default=False))
        
        # Adding field 'EmailMessage.is_deleted'
        db.add_column('mailing_emailmessage', 'is_deleted', models.BooleanField(_("Deleted"), default=False))
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'db_table': "'django_site'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'mailing.emailtemplate': {
            'Meta': {'ordering': "['-timestamp','name']"},
            'allowed_placeholders': ('models.ManyToManyField', ["orm['mailing.EmailTemplatePlaceholder']"], {'null': 'True', 'blank': 'True'}),
            'body': ('PlainTextModelField', ['_("Template Text (English)")'], {'blank': 'True'}),
            'body_de': ('PlainTextModelField', ['_("Template Text (German)")'], {'blank': 'True'}),
            'body_html': ('models.TextField', ['_("Template HTML (English)")'], {'null': 'True', 'blank': 'True'}),
            'body_html_de': ('models.TextField', ['_("Template HTML (German)")'], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', ['_("Template Name")'], {'max_length': '255'}),
            'owner': ('models.ForeignKey', ["orm['auth.User']"], {}),
            'site': ('models.ForeignKey', ["orm['sites.Site']"], {'null': 'True', 'blank': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'subject': ('models.CharField', ['_("Subject (English)")'], {'max_length': '255'}),
            'subject_de': ('models.CharField', ['_("Subject (German)")'], {'max_length': '255'}),
            'timestamp': ('models.DateTimeField', ['_("Written")'], {'auto_now_add': 'True'})
        },
        'mailing.emailtemplateplaceholder': {
            'Meta': {'ordering': "['relates_to','name']"},
            'help_text': ('models.CharField', ['_("Placeholder Help text")'], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('MultilingualCharField', ["_('Placeholder Name')"], {'unique': 'True', 'max_length': '64'}),
            'name_de': ('models.CharField', ["u'Placeholder Name'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '64', 'db_tablespace': "''", 'blank': 'False', 'unique': 'True', 'db_index': 'False'}),
            'name_en': ('models.CharField', ["u'Placeholder Name'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '64', 'db_tablespace': "''", 'blank': 'False', 'unique': 'True', 'db_index': 'False'}),
            'relates_to': ('models.IntegerField', ['_("relates to")'], {'default': '1'}),
            'sysname': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'timestamp': ('models.DateTimeField', ['_("Written")'], {'auto_now_add': 'True'})
        },
        'mailing.emailmessage': {
            'Meta': {'ordering': "('-timestamp','subject',)"},
            'body': ('PlainTextModelField', ['_("Message (Plain text)")'], {'blank': 'True'}),
            'body_html': ('ExtendedTextField', ['_("Message (HTML)")'], {'blank': 'True'}),
            'body_html_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'editable': 'False'}),
            'creator': ('models.ForeignKey', ["orm['auth.User']"], {'editable': 'False', 'related_name': '"%(class)s_creator"', 'null': 'True'}),
            'delete_after_sending': ('models.BooleanField', ['_("Delete after sending")'], {'default': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'is_sent': ('models.BooleanField', ['_("Sent")'], {'default': 'False'}),
            'modified_date': ('models.DateTimeField', ['_("modified date")'], {'null': 'True', 'editable': 'False'}),
            'modifier': ('models.ForeignKey', ["orm['auth.User']"], {'editable': 'False', 'related_name': '"%(class)s_modifier"', 'null': 'True'}),
            'recipient': ('models.ForeignKey', ["orm['auth.User']"], {'related_name': '"received_by_message_set"', 'null': 'True', 'blank': 'True'}),
            'recipient_emails': ('PlainTextModelField', ['_("Recipient email(s)")'], {'null': 'True', 'blank': 'True'}),
            'sender': ('models.ForeignKey', ["orm['auth.User']"], {'related_name': '"sent_by_message_set"', 'null': 'True', 'blank': 'True'}),
            'sender_email': ('models.EmailField', ['_("Sender email")'], {'null': 'True', 'blank': 'True'}),
            'sender_name': ('models.CharField', ['_("Sender name")'], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subject': ('models.CharField', ['_("Subject")'], {'max_length': '255', 'blank': 'True'}),
            'timestamp': ('models.DateTimeField', ['_("Written")'], {'auto_now_add': 'True'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['mailing']
