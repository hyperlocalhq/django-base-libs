# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Changing field 'PageSettings.site'
        db.alter_column('configuration_pagesettings', 'site_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'], unique=True))

        # Changing field 'PageSettings.path'
        db.alter_column('configuration_pagesettings', 'path', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'PageSettings.pickled_settings'
        db.alter_column('configuration_pagesettings', 'pickled_settings', self.gf('django.db.models.fields.TextField')())

        # Changing field 'PageSettings.user'
        db.alter_column('configuration_pagesettings', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True))

        # Deleting field 'sitesettings.gmaps_api_key'
        db.delete_column('configuration_sitesettings', 'gmaps_api_key')

        # Changing field 'SiteSettings.meta_description'
        db.alter_column('configuration_sitesettings', 'meta_description', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True))

        # Changing field 'SiteSettings.extra_head'
        db.alter_column('configuration_sitesettings', 'extra_head', self.gf('base_libs.models.fields.PlainTextModelField')())

        # Changing field 'SiteSettings.meta_keywords'
        db.alter_column('configuration_sitesettings', 'meta_keywords', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True))

        # Changing field 'SiteSettings.meta_author'
        db.alter_column('configuration_sitesettings', 'meta_author', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'SiteSettings.site'
        db.alter_column('configuration_sitesettings', 'site_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'], unique=True))

        # Changing field 'SiteSettings.meta_copyright'
        db.alter_column('configuration_sitesettings', 'meta_copyright', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'SiteSettings.login_by_email'
        db.alter_column('configuration_sitesettings', 'login_by_email', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'SiteSettings.extra_body'
        db.alter_column('configuration_sitesettings', 'extra_body', self.gf('base_libs.models.fields.PlainTextModelField')())

        # Changing field 'SiteSettings.registration_type'
        db.alter_column('configuration_sitesettings', 'registration_type', self.gf('django.db.models.fields.CharField')(max_length=10))
    
    
    def backwards(self, orm):
        
        # Changing field 'PageSettings.site'
        db.alter_column('configuration_pagesettings', 'site_id', self.gf('models.ForeignKey')(orm['sites.Site'], unique=True))

        # Changing field 'PageSettings.path'
        db.alter_column('configuration_pagesettings', 'path', self.gf('models.CharField')(_('Path'), max_length=100))

        # Changing field 'PageSettings.pickled_settings'
        db.alter_column('configuration_pagesettings', 'pickled_settings', self.gf('models.TextField')(_('Settings'), editable=False))

        # Changing field 'PageSettings.user'
        db.alter_column('configuration_pagesettings', 'user_id', self.gf('models.ForeignKey')(orm['auth.User'], null=True))

        # Adding field 'sitesettings.gmaps_api_key'
        db.add_column('configuration_sitesettings', 'gmaps_api_key', self.gf('models.CharField')(_("Google Maps API Key"), default='ABQIAAAACeM7_PeKjcwohDMmjxqD1RT1e54QDoeePfsGQUixHoyyb7eTxhTO-Ji1lhmrD0-TMcZt7uteQOa-GQ', max_length=200, blank=True), keep_default=False)

        # Changing field 'SiteSettings.meta_description'
        db.alter_column('configuration_sitesettings', 'meta_description', self.gf('MultilingualCharField')(_('Description'), max_length=255))

        # Changing field 'SiteSettings.extra_head'
        db.alter_column('configuration_sitesettings', 'extra_head', self.gf('PlainTextModelField')(_("Extra head")))

        # Changing field 'SiteSettings.meta_keywords'
        db.alter_column('configuration_sitesettings', 'meta_keywords', self.gf('MultilingualCharField')(_('Keywords'), max_length=255))

        # Changing field 'SiteSettings.meta_author'
        db.alter_column('configuration_sitesettings', 'meta_author', self.gf('models.CharField')(_('Author'), max_length=255))

        # Changing field 'SiteSettings.site'
        db.alter_column('configuration_sitesettings', 'site_id', self.gf('models.ForeignKey')(orm['sites.Site'], unique=True))

        # Changing field 'SiteSettings.meta_copyright'
        db.alter_column('configuration_sitesettings', 'meta_copyright', self.gf('models.CharField')(_('Copyright'), max_length=255))

        # Changing field 'SiteSettings.login_by_email'
        db.alter_column('configuration_sitesettings', 'login_by_email', self.gf('models.BooleanField')(_("Login by email")))

        # Changing field 'SiteSettings.extra_body'
        db.alter_column('configuration_sitesettings', 'extra_body', self.gf('PlainTextModelField')(_("Extra body")))

        # Changing field 'SiteSettings.registration_type'
        db.alter_column('configuration_sitesettings', 'registration_type', self.gf('models.CharField')(_("Registration type"), max_length=10))
    
    
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
        'configuration.pagesettings': {
            'Meta': {'ordering': "('path',)", 'object_name': 'PageSettings'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'pickled_settings': ('django.db.models.fields.TextField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']", 'unique': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        },
        'configuration.sitesettings': {
            'Meta': {'object_name': 'SiteSettings'},
            'extra_body': ('base_libs.models.fields.PlainTextModelField', [], {'blank': 'True'}),
            'extra_head': ('base_libs.models.fields.PlainTextModelField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login_by_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'meta_author': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'meta_copyright': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'meta_description': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'meta_description_de': ('django.db.models.fields.CharField', ["u'Description'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'meta_description_en': ('django.db.models.fields.CharField', ["u'Description'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'meta_keywords': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'meta_keywords_de': ('django.db.models.fields.CharField', ["u'Keywords'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'meta_keywords_en': ('django.db.models.fields.CharField', ["u'Keywords'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'registration_type': ('django.db.models.fields.CharField', [], {'default': "'simple'", 'max_length': '10'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']", 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('app_label', 'name')", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
    
    complete_apps = ['configuration']
