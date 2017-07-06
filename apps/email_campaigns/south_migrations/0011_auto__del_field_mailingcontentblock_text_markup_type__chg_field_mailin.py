# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Deleting field 'mailingcontentblock.text_markup_type'
        db.delete_column(u'email_campaigns_mailingcontentblock', 'text_markup_type')

        # Changing field 'MailingContentBlock.text_de'
        db.alter_column(u'email_campaigns_mailingcontentblock', 'text_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Text', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, unique=False, db_tablespace=''))

        # Changing field 'MailingContentBlock.title'
        db.alter_column(u'email_campaigns_mailingcontentblock', 'title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True))

        # Changing field 'MailingContentBlock.text'
        db.alter_column(u'email_campaigns_mailingcontentblock', 'text', self.gf('base_libs.models.fields.MultilingualTextField')(null=True))

        # Changing field 'MailingContentBlock.image'
        db.alter_column(u'email_campaigns_mailingcontentblock', 'image', self.gf('filebrowser.fields.FileBrowseField')(directory='newsletter/', max_length=255, extensions=['.jpg', '.jpeg', '.gif', '.png']))

        # Changing field 'MailingContentBlock.mailing'
        db.alter_column(u'email_campaigns_mailingcontentblock', 'mailing_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['email_campaigns.Mailing']))

        # Changing field 'MailingContentBlock.text_en'
        db.alter_column(u'email_campaigns_mailingcontentblock', 'text_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Text', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, unique=False, db_tablespace=''))

        # Changing field 'MailingContentBlock.topic'
        db.alter_column(u'email_campaigns_mailingcontentblock', 'topic', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True))

        # Changing field 'MailingContentBlock.link'
        db.alter_column(u'email_campaigns_mailingcontentblock', 'link', self.gf('django.db.models.fields.URLField')(max_length=200))

        # Changing field 'Campaign.title'
        db.alter_column(u'email_campaigns_campaign', 'title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True))

        # Deleting field 'mailing.body_html_markup_type'
        db.delete_column(u'email_campaigns_mailing', 'body_html_markup_type')

        # Changing field 'Mailing.status'
        db.alter_column(u'email_campaigns_mailing', 'status', self.gf('django.db.models.fields.PositiveIntegerField')())

        # Changing field 'Mailing.modified_date'
        db.alter_column(u'email_campaigns_mailing', 'modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Mailing.body_html_en'
        db.alter_column(u'email_campaigns_mailing', 'body_html_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Message', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, unique=False, db_tablespace=''))

        # Changing field 'Mailing.creator'
        db.alter_column(u'email_campaigns_mailing', 'creator_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'Mailing.sender_name'
        db.alter_column(u'email_campaigns_mailing', 'sender_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Mailing.body_html'
        db.alter_column(u'email_campaigns_mailing', 'body_html', self.gf('base_libs.models.fields.MultilingualTextField')(null=True))

        # Changing field 'Mailing.creation_date'
        db.alter_column(u'email_campaigns_mailing', 'creation_date', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Mailing.sender_email'
        db.alter_column(u'email_campaigns_mailing', 'sender_email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True))

        # Changing field 'Mailing.template'
        db.alter_column(u'email_campaigns_mailing', 'template', self.gf('base_libs.models.fields.TemplatePathField')(path='email_campaigns/mailing/', max_length=100, match='\\.html$'))

        # Changing field 'Mailing.modifier'
        db.alter_column(u'email_campaigns_mailing', 'modifier_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'Mailing.body_html_de'
        db.alter_column(u'email_campaigns_mailing', 'body_html_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Message', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, unique=False, db_tablespace=''))

        # Changing field 'Mailing.subject'
        db.alter_column(u'email_campaigns_mailing', 'subject', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True))

        # Changing field 'InfoSubscription.modified_date'
        db.alter_column(u'email_campaigns_infosubscription', 'modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'InfoSubscription.mailinglist'
        db.alter_column(u'email_campaigns_infosubscription', 'mailinglist_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['email_campaigns.MailingList']))

        # Changing field 'InfoSubscription.subscriber_name'
        db.alter_column(u'email_campaigns_infosubscription', 'subscriber_name', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'InfoSubscription.ip'
        db.alter_column(u'email_campaigns_infosubscription', 'ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15))

        # Changing field 'InfoSubscription.creation_date'
        db.alter_column(u'email_campaigns_infosubscription', 'creation_date', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'InfoSubscription.subscriber'
        db.alter_column(u'email_campaigns_infosubscription', 'subscriber_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True))

        # Changing field 'InfoSubscription.email'
        db.alter_column(u'email_campaigns_infosubscription', 'email', self.gf('django.db.models.fields.EmailField')(max_length=75))

        # Changing field 'MailingList.campaign'
        db.alter_column(u'email_campaigns_mailinglist', 'campaign_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['email_campaigns.Campaign'], null=True))

        # Changing field 'MailingList.title'
        db.alter_column(u'email_campaigns_mailinglist', 'title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True))

        # Changing field 'MailingList.site'
        db.alter_column(u'email_campaigns_mailinglist', 'site_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'], null=True))

        # Changing field 'MailingList.is_public'
        db.alter_column(u'email_campaigns_mailinglist', 'is_public', self.gf('django.db.models.fields.BooleanField')())
    
    
    def backwards(self, orm):
        
        # Adding field 'mailingcontentblock.text_markup_type'
        db.add_column(u'email_campaigns_mailingcontentblock', 'text_markup_type', self.gf('models.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Changing field 'MailingContentBlock.text_de'
        db.alter_column(u'email_campaigns_mailingcontentblock', 'text_de', self.gf('ExtendedTextField')(u'Text', db_tablespace='', unique_for_year=None, unique=False, unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=None, rel=None, unique_for_date=None))

        # Changing field 'MailingContentBlock.title'
        db.alter_column(u'email_campaigns_mailingcontentblock', 'title', self.gf('MultilingualCharField')(_("Title"), max_length=255))

        # Changing field 'MailingContentBlock.text'
        db.alter_column(u'email_campaigns_mailingcontentblock', 'text', self.gf('MultilingualTextField')(_("Text")))

        # Changing field 'MailingContentBlock.image'
        db.alter_column(u'email_campaigns_mailingcontentblock', 'image', self.gf('FileBrowseField')(_("Image"), directory="newsletter/", max_length=255, extensions=['.jpg','.jpeg','.gif','.png']))

        # Changing field 'MailingContentBlock.mailing'
        db.alter_column(u'email_campaigns_mailingcontentblock', 'mailing_id', self.gf('models.ForeignKey')(orm['email_campaigns.Mailing']))

        # Changing field 'MailingContentBlock.text_en'
        db.alter_column(u'email_campaigns_mailingcontentblock', 'text_en', self.gf('ExtendedTextField')(u'Text', db_tablespace='', unique_for_year=None, unique=False, unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=None, rel=None, unique_for_date=None))

        # Changing field 'MailingContentBlock.topic'
        db.alter_column(u'email_campaigns_mailingcontentblock', 'topic', self.gf('MultilingualCharField')(_("Topic"), max_length=255))

        # Changing field 'MailingContentBlock.link'
        db.alter_column(u'email_campaigns_mailingcontentblock', 'link', self.gf('models.URLField')(_("Link")))

        # Changing field 'Campaign.title'
        db.alter_column(u'email_campaigns_campaign', 'title', self.gf('MultilingualCharField')(_("Title"), max_length=255))

        # Adding field 'mailing.body_html_markup_type'
        db.add_column(u'email_campaigns_mailing', 'body_html_markup_type', self.gf('models.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Changing field 'Mailing.status'
        db.alter_column(u'email_campaigns_mailing', 'status', self.gf('models.PositiveIntegerField')(_("Status")))

        # Changing field 'Mailing.modified_date'
        db.alter_column(u'email_campaigns_mailing', 'modified_date', self.gf('models.DateTimeField')(_("modified date"), null=True, editable=False))

        # Changing field 'Mailing.body_html_en'
        db.alter_column(u'email_campaigns_mailing', 'body_html_en', self.gf('ExtendedTextField')(u'Message', db_tablespace='', unique_for_year=None, unique=False, unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=None, rel=None, unique_for_date=None))

        # Changing field 'Mailing.creator'
        db.alter_column(u'email_campaigns_mailing', 'creator_id', self.gf('models.ForeignKey')(orm['auth.User'], null=True, editable=False))

        # Changing field 'Mailing.sender_name'
        db.alter_column(u'email_campaigns_mailing', 'sender_name', self.gf('models.CharField')(_("Sender name"), max_length=255, null=True))

        # Changing field 'Mailing.body_html'
        db.alter_column(u'email_campaigns_mailing', 'body_html', self.gf('MultilingualTextField')(_("Message")))

        # Changing field 'Mailing.creation_date'
        db.alter_column(u'email_campaigns_mailing', 'creation_date', self.gf('models.DateTimeField')(_("creation date"), editable=False))

        # Changing field 'Mailing.sender_email'
        db.alter_column(u'email_campaigns_mailing', 'sender_email', self.gf('models.EmailField')(_("Sender email"), null=True))

        # Changing field 'Mailing.template'
        db.alter_column(u'email_campaigns_mailing', 'template', self.gf('TemplatePathField')(_("Template"), path="email_campaigns/mailing/", match="\.html$"))

        # Changing field 'Mailing.modifier'
        db.alter_column(u'email_campaigns_mailing', 'modifier_id', self.gf('models.ForeignKey')(orm['auth.User'], null=True, editable=False))

        # Changing field 'Mailing.body_html_de'
        db.alter_column(u'email_campaigns_mailing', 'body_html_de', self.gf('ExtendedTextField')(u'Message', db_tablespace='', unique_for_year=None, unique=False, unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=None, rel=None, unique_for_date=None))

        # Changing field 'Mailing.subject'
        db.alter_column(u'email_campaigns_mailing', 'subject', self.gf('MultilingualCharField')(_("Subject"), max_length=255))

        # Changing field 'InfoSubscription.modified_date'
        db.alter_column(u'email_campaigns_infosubscription', 'modified_date', self.gf('models.DateTimeField')(_("modified date"), null=True, editable=False))

        # Changing field 'InfoSubscription.mailinglist'
        db.alter_column(u'email_campaigns_infosubscription', 'mailinglist_id', self.gf('models.ForeignKey')(orm['email_campaigns.MailingList']))

        # Changing field 'InfoSubscription.subscriber_name'
        db.alter_column(u'email_campaigns_infosubscription', 'subscriber_name', self.gf('models.CharField')(_("Subscriber's name"), max_length=200))

        # Changing field 'InfoSubscription.ip'
        db.alter_column(u'email_campaigns_infosubscription', 'ip', self.gf('models.IPAddressField')(_("IP Address")))

        # Changing field 'InfoSubscription.creation_date'
        db.alter_column(u'email_campaigns_infosubscription', 'creation_date', self.gf('models.DateTimeField')(_("creation date"), editable=False))

        # Changing field 'InfoSubscription.subscriber'
        db.alter_column(u'email_campaigns_infosubscription', 'subscriber_id', self.gf('models.ForeignKey')(orm['auth.User'], null=True))

        # Changing field 'InfoSubscription.email'
        db.alter_column(u'email_campaigns_infosubscription', 'email', self.gf('models.EmailField')(_("Email address")))

        # Changing field 'MailingList.campaign'
        db.alter_column(u'email_campaigns_mailinglist', 'campaign_id', self.gf('models.ForeignKey')(orm['email_campaigns.Campaign'], null=True))

        # Changing field 'MailingList.title'
        db.alter_column(u'email_campaigns_mailinglist', 'title', self.gf('MultilingualCharField')(_("Title"), max_length=255))

        # Changing field 'MailingList.site'
        db.alter_column(u'email_campaigns_mailinglist', 'site_id', self.gf('models.ForeignKey')(orm['sites.Site'], null=True))

        # Changing field 'MailingList.is_public'
        db.alter_column(u'email_campaigns_mailinglist', 'is_public', self.gf('models.BooleanField')(_('Will this mailing list be displayed in the public settings of subscriptions?')))
    
    
    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'ordering': "('username',)", 'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 7, 2, 16, 16, 15, 641336)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 7, 2, 16, 16, 15, 640692)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('app_label', 'name')", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'email_campaigns.campaign': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Campaign'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        u'email_campaigns.infosubscription': {
            'Meta': {'ordering': "['email']", 'object_name': 'InfoSubscription'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'blank': 'True'}),
            'mailinglist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['email_campaigns.MailingList']"}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'subscriber': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'subscriber_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'email_campaigns.mailing': {
            'Meta': {'object_name': 'Mailing'},
            'body_html': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'body_html_de': ('base_libs.models.fields.ExtendedTextField', ["u'Message'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'body_html_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'body_html_en': ('base_libs.models.fields.ExtendedTextField', ["u'Message'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'body_html_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mailing_creator'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mailinglists': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['email_campaigns.MailingList']", 'symmetrical': 'False'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mailing_modifier'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'sender_email': ('django.db.models.fields.EmailField', [], {'default': "'ccb-contact@kulturprojekte-berlin.de'", 'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'sender_name': ('django.db.models.fields.CharField', [], {'default': "'Creative City Berlin'", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'subject': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subject_de': ('django.db.models.fields.CharField', ["u'Subject'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'subject_en': ('django.db.models.fields.CharField', ["u'Subject'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'template': ('base_libs.models.fields.TemplatePathField', [], {'path': "'email_campaigns/mailing/'", 'max_length': '100', 'match': "'\\\\.html$'"})
        },
        u'email_campaigns.mailingcontentblock': {
            'Meta': {'object_name': 'MailingContentBlock'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'directory': "'newsletter/'", 'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png']", 'blank': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'mailing': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['email_campaigns.Mailing']"}),
            'text': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'text_de': ('base_libs.models.fields.ExtendedTextField', ["u'Text'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'text_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'text_en': ('base_libs.models.fields.ExtendedTextField', ["u'Text'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'text_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'topic': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'topic_de': ('django.db.models.fields.CharField', ["u'Topic'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'topic_en': ('django.db.models.fields.CharField', ["u'Topic'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        u'email_campaigns.mailinglist': {
            'Meta': {'ordering': "('title', 'campaign')", 'object_name': 'MailingList'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['email_campaigns.Campaign']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']", 'null': 'True', 'blank': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['email_campaigns']
