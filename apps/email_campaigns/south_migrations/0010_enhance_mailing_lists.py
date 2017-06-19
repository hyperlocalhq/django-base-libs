# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from jetson.apps.email_campaigns.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'MailingList.is_public'
        db.add_column('email_campaigns_mailinglist', 'is_public', models.BooleanField(_('Will this mailing list be displayed in the public settings of subscriptions?'), default=True))
        
        # Adding field 'MailingList.site'
        db.add_column('email_campaigns_mailinglist', 'site', models.ForeignKey(orm['sites.Site'], null=True, blank=True))
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'MailingList.is_public'
        db.delete_column('email_campaigns_mailinglist', 'is_public')
        
        # Deleting field 'MailingList.site'
        db.delete_column('email_campaigns_mailinglist', 'site_id')
        
    
    
    models = {
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'db_table': "'django_site'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'email_campaigns.mailingcontentblock': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'image': ('FileBrowseField', ['_("Image")'], {'extensions': "['.jpg','.jpeg','.gif','.png']", 'max_length': '255', 'directory': '"newsletter/"', 'blank': 'True'}),
            'link': ('models.URLField', ['_("Link")'], {'blank': 'True'}),
            'mailing': ('models.ForeignKey', ["orm['email_campaigns.Mailing']"], {}),
            'text': ('MultilingualTextField', ['_("Text")'], {'blank': 'True'}),
            'text_de': ('ExtendedTextField', ["u'Text'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'text_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'text_en': ('ExtendedTextField', ["u'Text'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'text_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'text_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'title': ('MultilingualCharField', ['_("Title")'], {'max_length': '255', 'blank': 'True'}),
            'title_de': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'topic': ('MultilingualCharField', ['_("Topic")'], {'max_length': '255', 'blank': 'True'}),
            'topic_de': ('models.CharField', ["u'Topic'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'topic_en': ('models.CharField', ["u'Topic'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        'email_campaigns.mailing': {
            'body_html': ('MultilingualTextField', ['_("Message")'], {'blank': 'True'}),
            'body_html_de': ('ExtendedTextField', ["u'Message'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'body_html_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'body_html_en': ('ExtendedTextField', ["u'Message'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'body_html_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'body_html_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'editable': 'False'}),
            'creator': ('models.ForeignKey', ["orm['auth.User']"], {'editable': 'False', 'related_name': '"%(class)s_creator"', 'null': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'mailinglists': ('models.ManyToManyField', ["orm['email_campaigns.MailingList']"], {}),
            'modified_date': ('models.DateTimeField', ['_("modified date")'], {'null': 'True', 'editable': 'False'}),
            'modifier': ('models.ForeignKey', ["orm['auth.User']"], {'editable': 'False', 'related_name': '"%(class)s_modifier"', 'null': 'True'}),
            'sender_email': ('models.EmailField', ['_("Sender email")'], {'default': "'ccb-contact@kulturprojekte-berlin.de'", 'null': 'True', 'blank': 'True'}),
            'sender_name': ('models.CharField', ['_("Sender name")'], {'default': "'Creative City Berlin'", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'status': ('models.PositiveIntegerField', ['_("Status")'], {'default': '1'}),
            'subject': ('MultilingualCharField', ['_("Subject")'], {'max_length': '255', 'blank': 'True'}),
            'subject_de': ('models.CharField', ["u'Subject'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'subject_en': ('models.CharField', ["u'Subject'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'template': ('TemplatePathField', ['_("Template")'], {'path': '"email_campaigns/mailing/"', 'match': '"\\.html$"'})
        },
        'email_campaigns.infosubscription': {
            'Meta': {'ordering': "['email']"},
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'editable': 'False'}),
            'email': ('models.EmailField', ['_("Email address")'], {'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'ip': ('models.IPAddressField', ['_("IP Address")'], {'blank': 'True'}),
            'mailinglist': ('models.ForeignKey', ["orm['email_campaigns.MailingList']"], {}),
            'modified_date': ('models.DateTimeField', ['_("modified date")'], {'null': 'True', 'editable': 'False'}),
            'subscriber': ('models.ForeignKey', ["orm['auth.User']"], {'null': 'True', 'blank': 'True'}),
            'subscriber_name': ('models.CharField', ['_("Subscriber\'s name")'], {'max_length': '200', 'blank': 'True'})
        },
        'email_campaigns.campaign': {
            'Meta': {'ordering': "('title',)"},
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'title': ('MultilingualCharField', ['_("Title")'], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'email_campaigns.mailinglist': {
            'Meta': {'ordering': "('title','campaign',)"},
            'campaign': ('models.ForeignKey', ["orm['email_campaigns.Campaign']"], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('models.BooleanField', ["_('Will this mailing list be displayed in the public settings of subscriptions?')"], {'default': 'True'}),
            'site': ('models.ForeignKey', ["orm['sites.Site']"], {'null': 'True', 'blank': 'True'}),
            'title': ('MultilingualCharField', ['_("Title")'], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['email_campaigns']
