# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Changing field 'RowLevelPermission.owner_content_type'
        db.alter_column('auth_rowlevelpermission', 'owner_content_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType']))

        # Changing field 'RowLevelPermission.permission'
        db.alter_column('auth_rowlevelpermission', 'permission_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Permission']))

        # Changing field 'RowLevelPermission.object_id'
        db.alter_column('auth_rowlevelpermission', 'object_id', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'RowLevelPermission.owner_object_id'
        db.alter_column('auth_rowlevelpermission', 'owner_object_id', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'RowLevelPermission.content_type'
        db.alter_column('auth_rowlevelpermission', 'content_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType']))

        # Changing field 'PerObjectGroup.title'
        db.alter_column('auth_perobjectgroup', 'title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=80, null=True))

        # Changing field 'PerObjectGroup.object_id'
        db.alter_column('auth_perobjectgroup', 'object_id', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'PerObjectGroup.content_type'
        db.alter_column('auth_perobjectgroup', 'content_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType']))
    
    
    def backwards(self, orm):
        
        # Changing field 'RowLevelPermission.owner_content_type'
        db.alter_column('auth_rowlevelpermission', 'owner_content_type_id', self.gf('models.ForeignKey')(orm['contenttypes.ContentType'], null=False))

        # Changing field 'RowLevelPermission.permission'
        db.alter_column('auth_rowlevelpermission', 'permission_id', self.gf('models.ForeignKey')(orm['auth.Permission']))

        # Changing field 'RowLevelPermission.object_id'
        db.alter_column('auth_rowlevelpermission', 'object_id', self.gf('models.CharField')(u'Related object', max_length=255, null=False))

        # Changing field 'RowLevelPermission.owner_object_id'
        db.alter_column('auth_rowlevelpermission', 'owner_object_id', self.gf('models.CharField')(u'Owner', max_length=255, null=False))

        # Changing field 'RowLevelPermission.content_type'
        db.alter_column('auth_rowlevelpermission', 'content_type_id', self.gf('models.ForeignKey')(orm['contenttypes.ContentType'], null=False))

        # Changing field 'PerObjectGroup.title'
        db.alter_column('auth_perobjectgroup', 'title', self.gf('MultilingualCharField')(_('title'), max_length=80))

        # Changing field 'PerObjectGroup.object_id'
        db.alter_column('auth_perobjectgroup', 'object_id', self.gf('models.CharField')(u'Related object', max_length=255, null=False))

        # Changing field 'PerObjectGroup.content_type'
        db.alter_column('auth_perobjectgroup', 'content_type_id', self.gf('models.ForeignKey')(orm['contenttypes.ContentType'], null=False))
    
    
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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 7, 2, 16, 16, 35, 803673)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 7, 2, 16, 16, 35, 803109)'}),
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
        u'permissions.perobjectgroup': {
            'Meta': {'ordering': "('object_id', 'content_type')", 'object_name': 'PerObjectGroup', 'db_table': "'auth_perobjectgroup'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'sysname': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '80', 'db_index': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '80', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '80', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '80', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'permissions.rowlevelpermission': {
            'Meta': {'object_name': 'RowLevelPermission', 'db_table': "'auth_rowlevelpermission'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'negative': ('django.db.models.fields.BooleanField', [], {}),
            'object_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'owner_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owner'", 'to': u"orm['contenttypes.ContentType']"}),
            'owner_object_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Permission']"})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['permissions']
