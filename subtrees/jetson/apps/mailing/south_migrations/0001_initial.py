# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from jetson.apps.mailing.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'EmailTemplate'
        db.create_table('mailing_emailtemplate', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('site', models.ForeignKey(orm['sites.Site'], null=True, blank=True)),
            ('slug', models.SlugField(unique=True, max_length=255)),
            ('owner', models.ForeignKey(orm['auth.User'])),
            ('name', models.CharField(_("Template Name"), max_length=255)),
            ('subject', models.CharField(_("Subject (English)"), max_length=255)),
            ('subject_de', models.CharField(_("Subject (German)"), max_length=255)),
            ('body', PlainTextModelField(_("Template Text (English)"), blank=True)),
            ('body_de', PlainTextModelField(_("Template Text (German)"), blank=True)),
            ('body_html', models.TextField(_("Template HTML (English)"), null=True, blank=True)),
            ('body_html_de', models.TextField(_("Template HTML (German)"), null=True, blank=True)),
            ('timestamp', models.DateTimeField(_("Written"), auto_now_add=True)),
        )))
        db.send_create_signal('mailing', ['EmailTemplate'])
        
        # Adding model 'EmailTemplatePlaceholder'
        db.create_table('mailing_emailtemplateplaceholder', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('sysname', models.SlugField(unique=True, max_length=255)),
            ('name', MultilingualCharField(_('Placeholder Name'), unique=True, max_length=64)),
            ('relates_to', models.IntegerField(_("relates to"), default=1)),
            ('help_text', models.CharField(_("Placeholder Help text"), max_length=255, null=True, blank=True)),
            ('timestamp', models.DateTimeField(_("Written"), auto_now_add=True)),
            ('name_de', models.CharField(u'Placeholder Name', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=64, db_tablespace='', blank=False, unique=True, db_index=False)),
            ('name_en', models.CharField(u'Placeholder Name', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=64, db_tablespace='', blank=False, unique=True, db_index=False)),
        )))
        db.send_create_signal('mailing', ['EmailTemplatePlaceholder'])
        
        # Adding model 'EmailMessage'
        db.create_table('mailing_emailmessage', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('slug', models.SlugField(unique=True, max_length=255)),
            ('sender', models.ForeignKey(orm['auth.User'], related_name="sent_by_message_set", null=True, blank=True)),
            ('recipient', models.ForeignKey(orm['auth.User'], related_name="received_by_message_set", null=True, blank=True)),
            ('sender_name', models.CharField(_("Sender name"), max_length=255, null=True, blank=True)),
            ('sender_email', models.EmailField(_("Sender email"), null=True, blank=True)),
            ('recipient_emails', PlainTextModelField(_("Recipient email(s)"), null=True, blank=True)),
            ('subject', models.CharField(_("Subject"), max_length=255, blank=True)),
            ('body', PlainTextModelField(_("Message (Plain text)"), blank=True)),
            ('body_html', ExtendedTextField(_("Message (HTML)"), blank=True)),
            ('timestamp', models.DateTimeField(_("Written"), auto_now_add=True)),
            ('is_read', models.BooleanField(_("Read"), default=False)),
            ('is_deleted', models.BooleanField(_("Deleted"), default=False)),
            ('is_replied', models.BooleanField(_("Replied"), default=False)),
            ('is_spam', models.BooleanField(_("Spam"), default=False)),
            ('is_sent', models.BooleanField(_("Sent"), default=False)),
            ('is_internal', models.BooleanField(_("Internal"), default=False)),
            ('is_draft', models.BooleanField(_("Draft"), default=False)),
            ('delete_after_sending', models.BooleanField(_("Delete after sending"), default=False)),
            ('body_html_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
        )))
        db.send_create_signal('mailing', ['EmailMessage'])
        
        # Adding ManyToManyField 'EmailTemplate.allowed_placeholders'
        db.create_table('mailing_emailtemplate_allowed_placeholders', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('emailtemplate', models.ForeignKey(orm.EmailTemplate, null=False)),
            ('emailtemplateplaceholder', models.ForeignKey(orm.EmailTemplatePlaceholder, null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'EmailTemplate'
        db.delete_table('mailing_emailtemplate')
        
        # Deleting model 'EmailTemplatePlaceholder'
        db.delete_table('mailing_emailtemplateplaceholder')
        
        # Deleting model 'EmailMessage'
        db.delete_table('mailing_emailmessage')
        
        # Dropping ManyToManyField 'EmailTemplate.allowed_placeholders'
        db.delete_table('mailing_emailtemplate_allowed_placeholders')
        
    
    
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
            'delete_after_sending': ('models.BooleanField', ['_("Delete after sending")'], {'default': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'is_deleted': ('models.BooleanField', ['_("Deleted")'], {'default': 'False'}),
            'is_draft': ('models.BooleanField', ['_("Draft")'], {'default': 'False'}),
            'is_internal': ('models.BooleanField', ['_("Internal")'], {'default': 'False'}),
            'is_read': ('models.BooleanField', ['_("Read")'], {'default': 'False'}),
            'is_replied': ('models.BooleanField', ['_("Replied")'], {'default': 'False'}),
            'is_sent': ('models.BooleanField', ['_("Sent")'], {'default': 'False'}),
            'is_spam': ('models.BooleanField', ['_("Spam")'], {'default': 'False'}),
            'recipient': ('models.ForeignKey', ["orm['auth.User']"], {'related_name': '"received_by_message_set"', 'null': 'True', 'blank': 'True'}),
            'recipient_emails': ('PlainTextModelField', ['_("Recipient email(s)")'], {'null': 'True', 'blank': 'True'}),
            'sender': ('models.ForeignKey', ["orm['auth.User']"], {'related_name': '"sent_by_message_set"', 'null': 'True', 'blank': 'True'}),
            'sender_email': ('models.EmailField', ['_("Sender email")'], {'null': 'True', 'blank': 'True'}),
            'sender_name': ('models.CharField', ['_("Sender name")'], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'subject': ('models.CharField', ['_("Subject")'], {'max_length': '255', 'blank': 'True'}),
            'timestamp': ('models.DateTimeField', ['_("Written")'], {'auto_now_add': 'True'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['mailing']
