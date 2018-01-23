# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
                # Removing unique constraint on 'EmailTemplatePlaceholder', fields ['name_en']
        db.delete_unique(u'mailing_emailtemplateplaceholder', ['name_en'])

        # Removing unique constraint on 'EmailTemplatePlaceholder', fields ['name_de']
        db.delete_unique(u'mailing_emailtemplateplaceholder', ['name_de'])

        # Removing unique constraint on 'EmailTemplatePlaceholder', fields ['name']
        db.delete_unique(u'mailing_emailtemplateplaceholder', ['name'])

        # Adding field 'EmailTemplate.subject_fr'
        db.add_column(u'mailing_emailtemplate', 'subject_fr',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Adding field 'EmailTemplate.subject_pl'
        db.add_column(u'mailing_emailtemplate', 'subject_pl',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Adding field 'EmailTemplate.subject_tr'
        db.add_column(u'mailing_emailtemplate', 'subject_tr',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Adding field 'EmailTemplate.subject_es'
        db.add_column(u'mailing_emailtemplate', 'subject_es',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Adding field 'EmailTemplate.subject_it'
        db.add_column(u'mailing_emailtemplate', 'subject_it',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Adding field 'EmailTemplate.body_fr'
        db.add_column(u'mailing_emailtemplate', 'body_fr',
                      self.gf('base_libs.models.fields.PlainTextModelField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'EmailTemplate.body_pl'
        db.add_column(u'mailing_emailtemplate', 'body_pl',
                      self.gf('base_libs.models.fields.PlainTextModelField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'EmailTemplate.body_tr'
        db.add_column(u'mailing_emailtemplate', 'body_tr',
                      self.gf('base_libs.models.fields.PlainTextModelField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'EmailTemplate.body_es'
        db.add_column(u'mailing_emailtemplate', 'body_es',
                      self.gf('base_libs.models.fields.PlainTextModelField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'EmailTemplate.body_it'
        db.add_column(u'mailing_emailtemplate', 'body_it',
                      self.gf('base_libs.models.fields.PlainTextModelField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'EmailTemplate.body_html_fr'
        db.add_column(u'mailing_emailtemplate', 'body_html_fr',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'EmailTemplate.body_html_pl'
        db.add_column(u'mailing_emailtemplate', 'body_html_pl',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'EmailTemplate.body_html_tr'
        db.add_column(u'mailing_emailtemplate', 'body_html_tr',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'EmailTemplate.body_html_es'
        db.add_column(u'mailing_emailtemplate', 'body_html_es',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'EmailTemplate.body_html_it'
        db.add_column(u'mailing_emailtemplate', 'body_html_it',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'EmailTemplatePlaceholder.name_fr'
        db.add_column(u'mailing_emailtemplateplaceholder', 'name_fr',
                      self.gf('django.db.models.fields.CharField')(u'Placeholder Name', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=64, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'EmailTemplatePlaceholder.name_pl'
        db.add_column(u'mailing_emailtemplateplaceholder', 'name_pl',
                      self.gf('django.db.models.fields.CharField')(u'Placeholder Name', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=64, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'EmailTemplatePlaceholder.name_tr'
        db.add_column(u'mailing_emailtemplateplaceholder', 'name_tr',
                      self.gf('django.db.models.fields.CharField')(u'Placeholder Name', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=64, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'EmailTemplatePlaceholder.name_es'
        db.add_column(u'mailing_emailtemplateplaceholder', 'name_es',
                      self.gf('django.db.models.fields.CharField')(u'Placeholder Name', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=64, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'EmailTemplatePlaceholder.name_it'
        db.add_column(u'mailing_emailtemplateplaceholder', 'name_it',
                      self.gf('django.db.models.fields.CharField')(u'Placeholder Name', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=64, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

    
    
    def backwards(self, orm):
                # Deleting field 'EmailTemplate.subject_fr'
        db.delete_column(u'mailing_emailtemplate', 'subject_fr')

        # Deleting field 'EmailTemplate.subject_pl'
        db.delete_column(u'mailing_emailtemplate', 'subject_pl')

        # Deleting field 'EmailTemplate.subject_tr'
        db.delete_column(u'mailing_emailtemplate', 'subject_tr')

        # Deleting field 'EmailTemplate.subject_es'
        db.delete_column(u'mailing_emailtemplate', 'subject_es')

        # Deleting field 'EmailTemplate.subject_it'
        db.delete_column(u'mailing_emailtemplate', 'subject_it')

        # Deleting field 'EmailTemplate.body_fr'
        db.delete_column(u'mailing_emailtemplate', 'body_fr')

        # Deleting field 'EmailTemplate.body_pl'
        db.delete_column(u'mailing_emailtemplate', 'body_pl')

        # Deleting field 'EmailTemplate.body_tr'
        db.delete_column(u'mailing_emailtemplate', 'body_tr')

        # Deleting field 'EmailTemplate.body_es'
        db.delete_column(u'mailing_emailtemplate', 'body_es')

        # Deleting field 'EmailTemplate.body_it'
        db.delete_column(u'mailing_emailtemplate', 'body_it')

        # Deleting field 'EmailTemplate.body_html_fr'
        db.delete_column(u'mailing_emailtemplate', 'body_html_fr')

        # Deleting field 'EmailTemplate.body_html_pl'
        db.delete_column(u'mailing_emailtemplate', 'body_html_pl')

        # Deleting field 'EmailTemplate.body_html_tr'
        db.delete_column(u'mailing_emailtemplate', 'body_html_tr')

        # Deleting field 'EmailTemplate.body_html_es'
        db.delete_column(u'mailing_emailtemplate', 'body_html_es')

        # Deleting field 'EmailTemplate.body_html_it'
        db.delete_column(u'mailing_emailtemplate', 'body_html_it')

        # Deleting field 'EmailTemplatePlaceholder.name_fr'
        db.delete_column(u'mailing_emailtemplateplaceholder', 'name_fr')

        # Deleting field 'EmailTemplatePlaceholder.name_pl'
        db.delete_column(u'mailing_emailtemplateplaceholder', 'name_pl')

        # Deleting field 'EmailTemplatePlaceholder.name_tr'
        db.delete_column(u'mailing_emailtemplateplaceholder', 'name_tr')

        # Deleting field 'EmailTemplatePlaceholder.name_es'
        db.delete_column(u'mailing_emailtemplateplaceholder', 'name_es')

        # Deleting field 'EmailTemplatePlaceholder.name_it'
        db.delete_column(u'mailing_emailtemplateplaceholder', 'name_it')

        # Adding unique constraint on 'EmailTemplatePlaceholder', fields ['name']
        db.create_unique(u'mailing_emailtemplateplaceholder', ['name'])

        # Adding unique constraint on 'EmailTemplatePlaceholder', fields ['name_de']
        db.create_unique(u'mailing_emailtemplateplaceholder', ['name_de'])

        # Adding unique constraint on 'EmailTemplatePlaceholder', fields ['name_en']
        db.create_unique(u'mailing_emailtemplateplaceholder', ['name_en'])

    
    
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
        u'mailing.emailmessage': {
            'Meta': {'ordering': "('-creation_date', 'subject')", 'object_name': 'EmailMessage'},
            'body': ('base_libs.models.fields.PlainTextModelField', [], {'blank': 'True'}),
            'body_html': ('base_libs.models.fields.ExtendedTextField', [], {'blank': 'True'}),
            'body_html_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'emailmessage_creator'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'delete_after_sending': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'emailmessage_modifier'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'received_by_message_set'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'recipient_emails': ('base_libs.models.fields.PlainTextModelField', [], {'null': 'True', 'blank': 'True'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sent_by_message_set'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'sender_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'sender_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'mailing.emailtemplate': {
            'Meta': {'ordering': "['-timestamp', 'name']", 'object_name': 'EmailTemplate'},
            'allowed_placeholders': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['mailing.EmailTemplatePlaceholder']", 'null': 'True', 'blank': 'True'}),
            'body': ('base_libs.models.fields.PlainTextModelField', [], {'blank': 'True'}),
            'body_de': ('base_libs.models.fields.PlainTextModelField', [], {'blank': 'True'}),
            'body_es': ('base_libs.models.fields.PlainTextModelField', [], {'blank': 'True'}),
            'body_fr': ('base_libs.models.fields.PlainTextModelField', [], {'blank': 'True'}),
            'body_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'body_html_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'body_html_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'body_html_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'body_html_it': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'body_html_pl': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'body_html_tr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'body_it': ('base_libs.models.fields.PlainTextModelField', [], {'blank': 'True'}),
            'body_pl': ('base_libs.models.fields.PlainTextModelField', [], {'blank': 'True'}),
            'body_tr': ('base_libs.models.fields.PlainTextModelField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'subject_de': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'subject_es': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'subject_fr': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'subject_it': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'subject_pl': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'subject_tr': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'mailing.emailtemplateplaceholder': {
            'Meta': {'ordering': "['relates_to', 'name']", 'object_name': 'EmailTemplatePlaceholder'},
            'help_text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '64', 'null': 'True'}),
            'name_de': ('django.db.models.fields.CharField', ["u'Placeholder Name'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '64', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'name_en': ('django.db.models.fields.CharField', ["u'Placeholder Name'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '64', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'name_es': ('django.db.models.fields.CharField', ["u'Placeholder Name'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '64', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'name_fr': ('django.db.models.fields.CharField', ["u'Placeholder Name'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '64', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'name_it': ('django.db.models.fields.CharField', ["u'Placeholder Name'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '64', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'name_pl': ('django.db.models.fields.CharField', ["u'Placeholder Name'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '64', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'name_tr': ('django.db.models.fields.CharField', ["u'Placeholder Name'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '64', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'relates_to': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'sysname': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
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
    
    complete_apps = ['mailing']
