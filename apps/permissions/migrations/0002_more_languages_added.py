# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.utils.translation import ugettext_lazy as _

from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        # Changing field 'RowLevelPermission.owner_content_type'
        db.alter_column('auth_rowlevelpermission', 'owner_content_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType']))

        # Changing field 'RowLevelPermission.permission'
        db.alter_column('auth_rowlevelpermission', 'permission_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Permission']))

        # Changing field 'RowLevelPermission.content_type'
        db.alter_column('auth_rowlevelpermission', 'content_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType']))

        # Adding field 'PerObjectGroup.title_fr'
        db.add_column('auth_perobjectgroup', 'title_fr',
                      self.gf('django.db.models.fields.CharField')(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=80, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'PerObjectGroup.title_pl'
        db.add_column('auth_perobjectgroup', 'title_pl',
                      self.gf('django.db.models.fields.CharField')(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=80, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'PerObjectGroup.title_tr'
        db.add_column('auth_perobjectgroup', 'title_tr',
                      self.gf('django.db.models.fields.CharField')(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=80, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'PerObjectGroup.title_es'
        db.add_column('auth_perobjectgroup', 'title_es',
                      self.gf('django.db.models.fields.CharField')(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=80, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'PerObjectGroup.title_it'
        db.add_column('auth_perobjectgroup', 'title_it',
                      self.gf('django.db.models.fields.CharField')(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=80, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)


        # Changing field 'PerObjectGroup.title'
        db.alter_column('auth_perobjectgroup', 'title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=80, null=True))

        # Changing field 'PerObjectGroup.content_type'
        db.alter_column('auth_perobjectgroup', 'content_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType']))
    
    
    def backwards(self, orm):
        # Changing field 'RowLevelPermission.owner_content_type'
        db.alter_column('auth_rowlevelpermission', 'owner_content_type_id', self.gf('models.ForeignKey')(orm['contenttypes.ContentType'], null=False))

        # Changing field 'RowLevelPermission.permission'
        db.alter_column('auth_rowlevelpermission', 'permission_id', self.gf('models.ForeignKey')(orm['auth.Permission']))

        # Changing field 'RowLevelPermission.content_type'
        db.alter_column('auth_rowlevelpermission', 'content_type_id', self.gf('models.ForeignKey')(orm['contenttypes.ContentType'], null=False))

        # Deleting field 'PerObjectGroup.title_fr'
        db.delete_column('auth_perobjectgroup', 'title_fr')

        # Deleting field 'PerObjectGroup.title_pl'
        db.delete_column('auth_perobjectgroup', 'title_pl')

        # Deleting field 'PerObjectGroup.title_tr'
        db.delete_column('auth_perobjectgroup', 'title_tr')

        # Deleting field 'PerObjectGroup.title_es'
        db.delete_column('auth_perobjectgroup', 'title_es')

        # Deleting field 'PerObjectGroup.title_it'
        db.delete_column('auth_perobjectgroup', 'title_it')


        # Changing field 'PerObjectGroup.title'
        db.alter_column('auth_perobjectgroup', 'title', self.gf('MultilingualCharField')(_('title'), max_length=80))

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
        u'permissions.perobjectgroup': {
            'Meta': {'ordering': "('object_id', 'content_type')", 'object_name': 'PerObjectGroup', 'db_table': "'auth_perobjectgroup'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'sysname': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '80'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '80', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '80', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '80', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_es': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '80', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_fr': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '80', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_it': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '80', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_pl': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '80', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_tr': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '80', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False', 'blank': 'True'})
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
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['permissions']
