# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
                # Adding field 'SiteSettings.meta_keywords_fr'
        db.add_column(u'configuration_sitesettings', 'meta_keywords_fr',
                      self.gf('django.db.models.fields.CharField')(u'Keywords', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'SiteSettings.meta_keywords_pl'
        db.add_column(u'configuration_sitesettings', 'meta_keywords_pl',
                      self.gf('django.db.models.fields.CharField')(u'Keywords', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'SiteSettings.meta_keywords_tr'
        db.add_column(u'configuration_sitesettings', 'meta_keywords_tr',
                      self.gf('django.db.models.fields.CharField')(u'Keywords', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'SiteSettings.meta_keywords_es'
        db.add_column(u'configuration_sitesettings', 'meta_keywords_es',
                      self.gf('django.db.models.fields.CharField')(u'Keywords', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'SiteSettings.meta_keywords_it'
        db.add_column(u'configuration_sitesettings', 'meta_keywords_it',
                      self.gf('django.db.models.fields.CharField')(u'Keywords', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'SiteSettings.meta_description_fr'
        db.add_column(u'configuration_sitesettings', 'meta_description_fr',
                      self.gf('django.db.models.fields.CharField')(u'Description', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'SiteSettings.meta_description_pl'
        db.add_column(u'configuration_sitesettings', 'meta_description_pl',
                      self.gf('django.db.models.fields.CharField')(u'Description', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'SiteSettings.meta_description_tr'
        db.add_column(u'configuration_sitesettings', 'meta_description_tr',
                      self.gf('django.db.models.fields.CharField')(u'Description', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'SiteSettings.meta_description_es'
        db.add_column(u'configuration_sitesettings', 'meta_description_es',
                      self.gf('django.db.models.fields.CharField')(u'Description', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'SiteSettings.meta_description_it'
        db.add_column(u'configuration_sitesettings', 'meta_description_it',
                      self.gf('django.db.models.fields.CharField')(u'Description', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

    
    
    def backwards(self, orm):
                # Deleting field 'SiteSettings.meta_keywords_fr'
        db.delete_column(u'configuration_sitesettings', 'meta_keywords_fr')

        # Deleting field 'SiteSettings.meta_keywords_pl'
        db.delete_column(u'configuration_sitesettings', 'meta_keywords_pl')

        # Deleting field 'SiteSettings.meta_keywords_tr'
        db.delete_column(u'configuration_sitesettings', 'meta_keywords_tr')

        # Deleting field 'SiteSettings.meta_keywords_es'
        db.delete_column(u'configuration_sitesettings', 'meta_keywords_es')

        # Deleting field 'SiteSettings.meta_keywords_it'
        db.delete_column(u'configuration_sitesettings', 'meta_keywords_it')

        # Deleting field 'SiteSettings.meta_description_fr'
        db.delete_column(u'configuration_sitesettings', 'meta_description_fr')

        # Deleting field 'SiteSettings.meta_description_pl'
        db.delete_column(u'configuration_sitesettings', 'meta_description_pl')

        # Deleting field 'SiteSettings.meta_description_tr'
        db.delete_column(u'configuration_sitesettings', 'meta_description_tr')

        # Deleting field 'SiteSettings.meta_description_es'
        db.delete_column(u'configuration_sitesettings', 'meta_description_es')

        # Deleting field 'SiteSettings.meta_description_it'
        db.delete_column(u'configuration_sitesettings', 'meta_description_it')

    
    
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
        u'configuration.pagesettings': {
            'Meta': {'ordering': "('path',)", 'object_name': 'PageSettings'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'pickled_settings': ('django.db.models.fields.TextField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']", 'unique': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'})
        },
        u'configuration.sitesettings': {
            'Meta': {'object_name': 'SiteSettings'},
            'extra_body': ('base_libs.models.fields.PlainTextModelField', [], {'blank': 'True'}),
            'extra_head': ('base_libs.models.fields.PlainTextModelField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login_by_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'meta_author': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'meta_copyright': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'meta_description': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'meta_description_de': ('django.db.models.fields.CharField', ["u'Description'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'meta_description_en': ('django.db.models.fields.CharField', ["u'Description'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'meta_description_es': ('django.db.models.fields.CharField', ["u'Description'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'meta_description_fr': ('django.db.models.fields.CharField', ["u'Description'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'meta_description_it': ('django.db.models.fields.CharField', ["u'Description'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'meta_description_pl': ('django.db.models.fields.CharField', ["u'Description'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'meta_description_tr': ('django.db.models.fields.CharField', ["u'Description'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'meta_keywords': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'meta_keywords_de': ('django.db.models.fields.CharField', ["u'Keywords'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'meta_keywords_en': ('django.db.models.fields.CharField', ["u'Keywords'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'meta_keywords_es': ('django.db.models.fields.CharField', ["u'Keywords'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'meta_keywords_fr': ('django.db.models.fields.CharField', ["u'Keywords'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'meta_keywords_it': ('django.db.models.fields.CharField', ["u'Keywords'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'meta_keywords_pl': ('django.db.models.fields.CharField', ["u'Keywords'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'meta_keywords_tr': ('django.db.models.fields.CharField', ["u'Keywords'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'registration_type': ('django.db.models.fields.CharField', [], {'default': "'simple'", 'max_length': '10'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']", 'unique': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('app_label', 'name')", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
    
    complete_apps = ['configuration']
