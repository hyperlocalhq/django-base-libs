# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from jetson.apps.email_campaigns.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        from datetime import datetime
        
        # Adding model 'Campaign'
        db.create_table('email_campaigns_campaign', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('title', MultilingualCharField(_("Title"), max_length=255)),
            ('title_de', models.CharField(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('title_en', models.CharField(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
        )))
        db.send_create_signal('email_campaigns', ['Campaign'])
        
        # Adding model 'MailingContentBlock'
        db.create_table('email_campaigns_mailingcontentblock', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('topic', MultilingualCharField(_("Topic"), max_length=255, blank=True)),
            ('title', MultilingualCharField(_("Title"), max_length=255, blank=True)),
            ('text', MultilingualTextField(_("Text"), blank=True)),
            ('image', FileBrowseField(_("Image"), extensions=['.jpg','.jpeg','.gif','.png'], max_length=255, directory="/", blank=True)),
            ('mailing', models.ForeignKey(orm.Mailing)),
            ('title_de', models.CharField(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('title_en', models.CharField(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('text_de', ExtendedTextField(u'Text', unique_for_month=None, unique=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, null=False, unique_for_date=None, db_tablespace='', db_index=False)),
            ('text_de_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('text_en', ExtendedTextField(u'Text', unique_for_month=None, unique=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, null=False, unique_for_date=None, db_tablespace='', db_index=False)),
            ('text_en_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('text_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('topic_de', models.CharField(u'Topic', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('topic_en', models.CharField(u'Topic', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
        )))
        db.send_create_signal('email_campaigns', ['MailingContentBlock'])
        
        # Adding model 'Mailing'
        db.create_table('email_campaigns_mailing', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('creation_date', models.DateTimeField(_("creation date"), editable=False)),
            ('modified_date', models.DateTimeField(_("modified date"), null=True, editable=False)),
            ('creator', models.ForeignKey(orm['auth.User'], editable=False, related_name="%(class)s_creator", null=True)),
            ('modifier', models.ForeignKey(orm['auth.User'], editable=False, related_name="%(class)s_modifier", null=True)),
            ('sender_name', models.CharField(_("Sender name"), max_length=255, null=True, blank=True)),
            ('sender_email', models.EmailField(_("Sender email"), null=True, blank=True)),
            ('subject', MultilingualCharField(_("Subject"), max_length=255, blank=True)),
            ('body_html', MultilingualTextField(_("Message"), blank=True)),
            ('body_html_de', ExtendedTextField(u'Message', unique_for_month=None, unique=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, null=False, unique_for_date=None, db_tablespace='', db_index=False)),
            ('body_html_de_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('body_html_en', ExtendedTextField(u'Message', unique_for_month=None, unique=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, null=False, unique_for_date=None, db_tablespace='', db_index=False)),
            ('body_html_en_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('body_html_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('subject_de', models.CharField(u'Subject', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('subject_en', models.CharField(u'Subject', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
        )))
        db.send_create_signal('email_campaigns', ['Mailing'])
        
        # Adding model 'MailingList'
        db.create_table('email_campaigns_mailinglist', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('campaign', models.ForeignKey(orm.Campaign)),
            ('title', MultilingualCharField(_("Title"), max_length=255)),
            ('title_de', models.CharField(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('title_en', models.CharField(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
        )))
        db.send_create_signal('email_campaigns', ['MailingList'])
        
        # Adding field 'InfoSubscription.modified_date'
        db.add_column('email_campaigns_infosubscription', 'modified_date', models.DateTimeField(_("modified date"), null=True, editable=False))
        
        # Adding field 'InfoSubscription.mailinglist'
        db.add_column('email_campaigns_infosubscription', 'mailinglist', models.ForeignKey(orm.MailingList, null=True))
        
        # Adding field 'InfoSubscription.creation_date'
        db.add_column('email_campaigns_infosubscription', 'creation_date', models.DateTimeField(_("creation date"), editable=False, default=datetime.now))
        
        # Adding ManyToManyField 'Mailing.mailinglists'
        db.create_table('email_campaigns_mailing_mailinglists', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mailing', models.ForeignKey(orm.Mailing, null=True)),
            ('mailinglist', models.ForeignKey(orm.MailingList, null=True))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Campaign'
        db.delete_table('email_campaigns_campaign')
        
        # Deleting model 'MailingContentBlock'
        db.delete_table('email_campaigns_mailingcontentblock')
        
        # Deleting model 'Mailing'
        db.delete_table('email_campaigns_mailing')
        
        # Deleting model 'MailingList'
        db.delete_table('email_campaigns_mailinglist')
        
        # Deleting field 'InfoSubscription.modified_date'
        db.delete_column('email_campaigns_infosubscription', 'modified_date')
        
        # Deleting field 'InfoSubscription.mailinglist'
        db.delete_column('email_campaigns_infosubscription', 'mailinglist_id')
        
        # Deleting field 'InfoSubscription.creation_date'
        db.delete_column('email_campaigns_infosubscription', 'creation_date')
        
        # Dropping ManyToManyField 'Mailing.mailinglists'
        db.delete_table('email_campaigns_mailing_mailinglists')
        
    
    
    models = {
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'db_table': "'django_site'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'email_campaigns.mailingcontentblock': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'image': ('FileBrowseField', ['_("Image")'], {'extensions': "['.jpg','.jpeg','.gif','.png']", 'max_length': '255', 'directory': '"/"', 'blank': 'True'}),
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
            'sender_email': ('models.EmailField', ['_("Sender email")'], {'null': 'True', 'blank': 'True'}),
            'sender_name': ('models.CharField', ['_("Sender name")'], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subject': ('MultilingualCharField', ['_("Subject")'], {'max_length': '255', 'blank': 'True'}),
            'subject_de': ('models.CharField', ["u'Subject'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'subject_en': ('models.CharField', ["u'Subject'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        'email_campaigns.infosubscription': {
            'Meta': {'ordering': "['email']"},
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'editable': 'False'}),
            'email': ('models.EmailField', ['_("Email address")'], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'ip': ('models.IPAddressField', ['_("IP Address")'], {}),
            'mailinglist': ('models.ForeignKey', ["orm['email_campaigns.MailingList']"], {}),
            'modified_date': ('models.DateTimeField', ['_("modified date")'], {'null': 'True', 'editable': 'False'}),
            'site': ('models.ForeignKey', ["orm['sites.Site']"], {'null': 'True', 'blank': 'True'}),
            'subscriber': ('models.ForeignKey', ["orm['auth.User']"], {'null': 'True', 'blank': 'True'}),
            'subscriber_name': ('models.CharField', ['_("Subscriber\'s name")'], {'max_length': '200'}),
            'timestamp': ('models.DateTimeField', ['_("Timestamp")'], {'auto_now_add': 'True'})
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
            'campaign': ('models.ForeignKey', ["orm['email_campaigns.Campaign']"], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'title': ('MultilingualCharField', ['_("Title")'], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['email_campaigns']
