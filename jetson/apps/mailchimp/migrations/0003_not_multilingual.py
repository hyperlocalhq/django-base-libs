# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Deleting field 'MailingContentBlock.title_de'
        db.delete_column('mailchimp_mailingcontentblock', 'title_de')

        # Deleting field 'MailingContentBlock.topic_de'
        db.delete_column('mailchimp_mailingcontentblock', 'topic_de')

        # Deleting field 'MailingContentBlock.text_de'
        db.delete_column('mailchimp_mailingcontentblock', 'text_de')

        # Deleting field 'MailingContentBlock.title_en'
        db.delete_column('mailchimp_mailingcontentblock', 'title_en')

        # Deleting field 'MailingContentBlock.text_en'
        db.delete_column('mailchimp_mailingcontentblock', 'text_en')

        # Deleting field 'MailingContentBlock.topic_en'
        db.delete_column('mailchimp_mailingcontentblock', 'topic_en')

        # Deleting field 'MailingContentBlock.text_en_markup_type'
        db.delete_column('mailchimp_mailingcontentblock', 'text_en_markup_type')

        # Deleting field 'MailingContentBlock.text_de_markup_type'
        db.delete_column('mailchimp_mailingcontentblock', 'text_de_markup_type')

        # Changing field 'MailingContentBlock.title'
        db.alter_column('mailchimp_mailingcontentblock', 'title', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'MailingContentBlock.text'
        db.alter_column('mailchimp_mailingcontentblock', 'text', self.gf('base_libs.models.fields.ExtendedTextField')(default=''))

        # Changing field 'MailingContentBlock.topic'
        db.alter_column('mailchimp_mailingcontentblock', 'topic', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Deleting field 'Campaign.subject_de'
        db.delete_column('mailchimp_campaign', 'subject_de')

        # Deleting field 'Campaign.body_html_de_markup_type'
        db.delete_column('mailchimp_campaign', 'body_html_de_markup_type')

        # Deleting field 'Campaign.body_html_en_markup_type'
        db.delete_column('mailchimp_campaign', 'body_html_en_markup_type')

        # Deleting field 'Campaign.body_html_en'
        db.delete_column('mailchimp_campaign', 'body_html_en')

        # Deleting field 'Campaign.subject_en'
        db.delete_column('mailchimp_campaign', 'subject_en')

        # Deleting field 'Campaign.body_html_de'
        db.delete_column('mailchimp_campaign', 'body_html_de')

        # Changing field 'Campaign.body_html'
        db.alter_column('mailchimp_campaign', 'body_html', self.gf('base_libs.models.fields.ExtendedTextField')(default=''))

        # Changing field 'Campaign.template'
        db.alter_column('mailchimp_campaign', 'template', self.gf('base_libs.models.fields.TemplatePathField')(path='mailchimp/campaign/', max_length=100, match='\\.html$'))

        # Changing field 'Campaign.subject'
        db.alter_column('mailchimp_campaign', 'subject', self.gf('django.db.models.fields.CharField')(default='', max_length=255))
    
    
    def backwards(self, orm):
        
        # Adding field 'MailingContentBlock.title_de'
        db.add_column('mailchimp_mailingcontentblock', 'title_de', self.gf('django.db.models.fields.CharField')(u'Title', unique=False, max_length=255, primary_key=False, db_column=None, blank=True, default='', null=False, editable=True, db_tablespace='', db_index=False), keep_default=False)

        # Adding field 'MailingContentBlock.topic_de'
        db.add_column('mailchimp_mailingcontentblock', 'topic_de', self.gf('django.db.models.fields.CharField')(u'Topic', unique=False, max_length=255, primary_key=False, db_column=None, blank=True, default='', null=False, editable=True, db_tablespace='', db_index=False), keep_default=False)

        # Adding field 'MailingContentBlock.text_de'
        db.add_column('mailchimp_mailingcontentblock', 'text_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Text', rel=None, unique_for_year=None, blank=True, unique_for_date=None, db_index=False, unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, db_tablespace=''), keep_default=False)

        # Adding field 'MailingContentBlock.title_en'
        db.add_column('mailchimp_mailingcontentblock', 'title_en', self.gf('django.db.models.fields.CharField')(u'Title', unique=False, max_length=255, primary_key=False, db_column=None, blank=True, default='', null=False, editable=True, db_tablespace='', db_index=False), keep_default=False)

        # Adding field 'MailingContentBlock.text_en'
        db.add_column('mailchimp_mailingcontentblock', 'text_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Text', rel=None, unique_for_year=None, blank=True, unique_for_date=None, db_index=False, unique_for_month=None, unique=False, primary_key=False, db_column=None, max_length=None, db_tablespace=''), keep_default=False)

        # Adding field 'MailingContentBlock.topic_en'
        db.add_column('mailchimp_mailingcontentblock', 'topic_en', self.gf('django.db.models.fields.CharField')(u'Topic', unique=False, max_length=255, primary_key=False, db_column=None, blank=True, default='', null=False, editable=True, db_tablespace='', db_index=False), keep_default=False)

        # Adding field 'MailingContentBlock.text_en_markup_type'
        db.add_column('mailchimp_mailingcontentblock', 'text_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'MailingContentBlock.text_de_markup_type'
        db.add_column('mailchimp_mailingcontentblock', 'text_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Changing field 'MailingContentBlock.title'
        db.alter_column('mailchimp_mailingcontentblock', 'title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True))

        # Changing field 'MailingContentBlock.text'
        db.alter_column('mailchimp_mailingcontentblock', 'text', self.gf('base_libs.models.fields.MultilingualTextField')(null=True))

        # Changing field 'MailingContentBlock.topic'
        db.alter_column('mailchimp_mailingcontentblock', 'topic', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True))

        # Adding field 'Campaign.subject_de'
        db.add_column('mailchimp_campaign', 'subject_de', self.gf('django.db.models.fields.CharField')(u'Subject', unique=False, max_length=255, primary_key=False, db_column=None, blank=True, default='', null=False, editable=True, db_tablespace='', db_index=False), keep_default=False)

        # Adding field 'Campaign.body_html_de_markup_type'
        db.add_column('mailchimp_campaign', 'body_html_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Campaign.body_html_en_markup_type'
        db.add_column('mailchimp_campaign', 'body_html_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Campaign.body_html_en'
        db.add_column('mailchimp_campaign', 'body_html_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Message', rel=None, unique_for_year=None, blank=True, unique_for_date=None, db_index=False, unique_for_month=None, unique=False, primary_key=False, db_column=None, max_length=None, db_tablespace=''), keep_default=False)

        # Adding field 'Campaign.subject_en'
        db.add_column('mailchimp_campaign', 'subject_en', self.gf('django.db.models.fields.CharField')(u'Subject', unique=False, max_length=255, primary_key=False, db_column=None, blank=True, default='', null=False, editable=True, db_tablespace='', db_index=False), keep_default=False)

        # Adding field 'Campaign.body_html_de'
        db.add_column('mailchimp_campaign', 'body_html_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Message', rel=None, unique_for_year=None, blank=True, unique_for_date=None, db_index=False, unique_for_month=None, unique=False, primary_key=False, db_column=None, max_length=None, db_tablespace=''), keep_default=False)

        # Changing field 'Campaign.body_html'
        db.alter_column('mailchimp_campaign', 'body_html', self.gf('base_libs.models.fields.MultilingualTextField')(null=True))

        # Changing field 'Campaign.template'
        db.alter_column('mailchimp_campaign', 'template', self.gf('base_libs.models.fields.TemplatePathField')(path='mailchimp/mailing/', max_length=100, match='\\.html$'))

        # Changing field 'Campaign.subject'
        db.alter_column('mailchimp_campaign', 'subject', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True))
    
    
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'ordering': "('username',)", 'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('app_label', 'name')", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'mailchimp.campaign': {
            'Meta': {'ordering': "('-creation_date',)", 'object_name': 'Campaign'},
            'body_html': ('base_libs.models.fields.ExtendedTextField', [], {'blank': 'True'}),
            'body_html_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'campaign_creator'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mailinglist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mailchimp.MList']"}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'campaign_modifier'", 'null': 'True', 'to': "orm['auth.User']"}),
            'sender_email': ('django.db.models.fields.EmailField', [], {'default': "'ccb-contact@kulturprojekte-berlin.de'", 'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'sender_name': ('django.db.models.fields.CharField', [], {'default': "'Creative City Berlin'", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'template': ('base_libs.models.fields.TemplatePathField', [], {'path': "'mailchimp/campaign/'", 'max_length': '100', 'match': "'\\\\.html$'"})
        },
        'mailchimp.mailingcontentblock': {
            'Meta': {'object_name': 'MailingContentBlock'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mailchimp.Campaign']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'directory': "'newsletter/'", 'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png']", 'blank': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'text': ('base_libs.models.fields.ExtendedTextField', [], {'blank': 'True'}),
            'text_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'mailchimp.mlist': {
            'Meta': {'ordering': "['title']", 'object_name': 'MList'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_sync': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']", 'null': 'True', 'blank': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'mailchimp.settings': {
            'Meta': {'ordering': "['api_key']", 'object_name': 'Settings'},
            'api_key': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'delete_member': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'double_optin': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'send_goodbye': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'send_welcome': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'update_existing': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'mailchimp.subscription': {
            'Meta': {'ordering': "['email']", 'object_name': 'Subscription'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'mailinglist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mailchimp.MList']"}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'subscriber': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'permissions.rowlevelpermission': {
            'Meta': {'object_name': 'RowLevelPermission', 'db_table': "'auth_rowlevelpermission'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'negative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'owner_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owner'", 'to': "orm['contenttypes.ContentType']"}),
            'owner_object_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.Permission']"})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['mailchimp']
