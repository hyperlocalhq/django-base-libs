# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Settings'
        db.create_table(u'mailchimp_settings', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('api_key', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('double_optin', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('update_existing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('send_welcome', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('delete_member', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('send_goodbye', self.gf('django.db.models.fields.BooleanField')(default=True)),
        )))
        db.send_create_signal(u'mailchimp', ['Settings'])

        # Adding model 'Subscription'
        db.create_table(u'mailchimp_subscription', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('subscriber', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, blank=True)),
            ('mailinglist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mailchimp.MList'])),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        )))
        db.send_create_signal(u'mailchimp', ['Subscription'])

        # Adding model 'MList'
        db.create_table(u'mailchimp_mlist', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'], null=True, blank=True)),
            ('title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('last_sync', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('title_de', self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('title_en', self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
        )))
        db.send_create_signal(u'mailchimp', ['MList'])

        # Adding model 'Campaign'
        db.create_table(u'mailchimp_campaign', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='campaign_creator', null=True, to=orm['auth.User'])),
            ('modifier', self.gf('django.db.models.fields.related.ForeignKey')(related_name='campaign_modifier', null=True, to=orm['auth.User'])),
            ('sender_name', self.gf('django.db.models.fields.CharField')(default='Berlin B\xc3\xbchnen', max_length=255)),
            ('sender_email', self.gf('django.db.models.fields.EmailField')(default='kontakt@berlinbuehnen.de', max_length=75)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('body_html', self.gf('base_libs.models.fields.ExtendedTextField')(blank=True)),
            ('mailinglist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mailchimp.MList'])),
            ('template', self.gf('base_libs.models.fields.TemplatePathField')(path='mailchimp/campaign/', max_length=100, match='\\.html$')),
            ('status', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('body_html_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
        )))
        db.send_create_signal(u'mailchimp', ['Campaign'])

        # Adding model 'MailingContentBlock'
        db.create_table(u'mailchimp_mailingcontentblock', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mailchimp.Campaign'])),
            ('content_type', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('content', self.gf('base_libs.models.fields.ExtendedTextField')(blank=True)),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('content_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
        )))
        db.send_create_signal(u'mailchimp', ['MailingContentBlock'])
    
    
    def backwards(self, orm):
                # Deleting model 'Settings'
        db.delete_table(u'mailchimp_settings')

        # Deleting model 'Subscription'
        db.delete_table(u'mailchimp_subscription')

        # Deleting model 'MList'
        db.delete_table(u'mailchimp_mlist')

        # Deleting model 'Campaign'
        db.delete_table(u'mailchimp_campaign')

        # Deleting model 'MailingContentBlock'
        db.delete_table(u'mailchimp_mailingcontentblock')

    
    
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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('app_label', 'name')", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'mailchimp.campaign': {
            'Meta': {'ordering': "('-creation_date',)", 'object_name': 'Campaign'},
            'body_html': ('base_libs.models.fields.ExtendedTextField', [], {'blank': 'True'}),
            'body_html_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'campaign_creator'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mailinglist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mailchimp.MList']"}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'campaign_modifier'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'sender_email': ('django.db.models.fields.EmailField', [], {'default': "'kontakt@berlinbuehnen.de'", 'max_length': '75'}),
            'sender_name': ('django.db.models.fields.CharField', [], {'default': "'Berlin B\\xc3\\xbchnen'", 'max_length': '255'}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'template': ('base_libs.models.fields.TemplatePathField', [], {'path': "'mailchimp/campaign/'", 'max_length': '100', 'match': "'\\\\.html$'"})
        },
        u'mailchimp.mailingcontentblock': {
            'Meta': {'ordering': "('sort_order',)", 'object_name': 'MailingContentBlock'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mailchimp.Campaign']"}),
            'content': ('base_libs.models.fields.ExtendedTextField', [], {'blank': 'True'}),
            'content_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'content_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': 'None'})
        },
        u'mailchimp.mlist': {
            'Meta': {'ordering': "['title']", 'object_name': 'MList'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_sync': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']", 'null': 'True', 'blank': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        u'mailchimp.settings': {
            'Meta': {'ordering': "['api_key']", 'object_name': 'Settings'},
            'api_key': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'delete_member': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'double_optin': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'send_goodbye': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'send_welcome': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'update_existing': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'mailchimp.subscription': {
            'Meta': {'ordering': "['email']", 'object_name': 'Subscription'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'mailinglist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mailchimp.MList']"}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'subscriber': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'permissions.rowlevelpermission': {
            'Meta': {'object_name': 'RowLevelPermission', 'db_table': "'auth_rowlevelpermission'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'negative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'owner_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owner'", 'to': u"orm['contenttypes.ContentType']"}),
            'owner_object_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Permission']"})
        },
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['mailchimp']
