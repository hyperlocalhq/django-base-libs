# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.conf import settings
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        for lang_code, lang_name in settings.LANGUAGES:
            if lang_code not in ("de", ):
                # Adding field 'ExtendedLogEntry.change_message_en'
                db.add_column(u'history_extendedlogentry', 'change_message_%s' % lang_code,
                      self.gf('base_libs.models.fields.PlainTextModelField')(u'change message', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Changing field 'ExtendedLogEntry.change_message_de'
        db.alter_column(u'history_extendedlogentry', 'change_message_de', self.gf('base_libs.models.fields.PlainTextModelField')(u'change message', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, unique=False, db_tablespace=''))


        # Changing field 'ExtendedLogEntry.action_flag'
        db.alter_column(u'history_extendedlogentry', 'action_flag', self.gf('django.db.models.fields.PositiveSmallIntegerField')())

        # Changing field 'ExtendedLogEntry.action_time'
        db.alter_column(u'history_extendedlogentry', 'action_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'ExtendedLogEntry.object_repr'
        db.alter_column(u'history_extendedlogentry', 'object_repr', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'ExtendedLogEntry.change_message'
        db.alter_column(u'history_extendedlogentry', 'change_message', self.gf('base_libs.models.fields.MultilingualPlainTextField')(null=True))

        # Changing field 'ExtendedLogEntry.user'
        db.alter_column(u'history_extendedlogentry', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'ExtendedLogEntry.content_type'
        db.alter_column(u'history_extendedlogentry', 'content_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True))

        # Changing field 'ExtendedLogEntry.scope'
        db.alter_column(u'history_extendedlogentry', 'scope', self.gf('django.db.models.fields.PositiveSmallIntegerField')())


    
    def backwards(self, orm):
        for lang_code, lang_name in settings.LANGUAGES:
            if lang_code not in ("de", ):
                # Deleting field 'ExtendedLogEntry.change_message_en'
                db.delete_column(u'history_extendedlogentry', 'change_message_%s' % lang_code)

        # Changing field 'ExtendedLogEntry.change_message_de'
        db.alter_column(u'history_extendedlogentry', 'change_message_de', self.gf('models.TextField')(_('change message'), default=''))

        # Changing field 'ExtendedLogEntry.action_flag'
        db.alter_column(u'history_extendedlogentry', 'action_flag', self.gf('models.PositiveSmallIntegerField')(_('action')))

        # Changing field 'ExtendedLogEntry.action_time'
        db.alter_column(u'history_extendedlogentry', 'action_time', self.gf('models.DateTimeField')(_('action time'), auto_now=True))

        # Changing field 'ExtendedLogEntry.object_repr'
        db.alter_column(u'history_extendedlogentry', 'object_repr', self.gf('models.CharField')(_('object repr'), max_length=200))

        # Changing field 'ExtendedLogEntry.change_message'
        db.alter_column(u'history_extendedlogentry', 'change_message', self.gf('models.TextField')(_('change message'), default=''))

        # Changing field 'ExtendedLogEntry.user'
        db.alter_column(u'history_extendedlogentry', 'user_id', self.gf('models.ForeignKey')(orm['auth.User']))

        # Changing field 'ExtendedLogEntry.content_type'
        db.alter_column(u'history_extendedlogentry', 'content_type_id', self.gf('models.ForeignKey')(orm['contenttypes.ContentType'], limit_choices_to={}, null=True))

        # Changing field 'ExtendedLogEntry.scope'
        db.alter_column(u'history_extendedlogentry', 'scope', self.gf('models.PositiveSmallIntegerField')(_('scope')))

    
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
        u'history.extendedlogentry': {
            'Meta': {'ordering': "('-action_time',)", 'object_name': 'ExtendedLogEntry'},
            'action_flag': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'action_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'change_message': ('base_libs.models.fields.MultilingualPlainTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'change_message_de': ('base_libs.models.fields.PlainTextModelField', ["u'change message'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'change_message_en': ('base_libs.models.fields.PlainTextModelField', ["u'change message'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'change_message_es': ('base_libs.models.fields.PlainTextModelField', ["u'change message'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'change_message_fr': ('base_libs.models.fields.PlainTextModelField', ["u'change message'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'change_message_it': ('base_libs.models.fields.PlainTextModelField', ["u'change message'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'change_message_pl': ('base_libs.models.fields.PlainTextModelField', ["u'change message'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'change_message_tr': ('base_libs.models.fields.PlainTextModelField', ["u'change message'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'object_repr': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'scope': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
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
    
    complete_apps = ['history']
