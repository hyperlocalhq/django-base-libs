# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
                # Deleting field 'Person.involvement_role_de'
        db.delete_column(u'people_person', 'involvement_role_de')

        # Deleting field 'Person.involvement_instrument_de'
        db.delete_column(u'people_person', 'involvement_instrument_de')

        # Deleting field 'Person.involvement_instrument'
        db.delete_column(u'people_person', 'involvement_instrument')

        # Deleting field 'Person.authorship_type'
        db.delete_column(u'people_person', 'authorship_type_id')

        # Deleting field 'Person.leadership_function_de'
        db.delete_column(u'people_person', 'leadership_function_de')

        # Deleting field 'Person.involvement_type'
        db.delete_column(u'people_person', 'involvement_type_id')

        # Deleting field 'Person.leadership_function'
        db.delete_column(u'people_person', 'leadership_function')

        # Deleting field 'Person.involvement_role_en'
        db.delete_column(u'people_person', 'involvement_role_en')

        # Deleting field 'Person.involvement_instrument_en'
        db.delete_column(u'people_person', 'involvement_instrument_en')

        # Deleting field 'Person.involvement_role'
        db.delete_column(u'people_person', 'involvement_role')

        # Deleting field 'Person.leadership_function_en'
        db.delete_column(u'people_person', 'leadership_function_en')

    
    
    def backwards(self, orm):
                # Adding field 'Person.involvement_role_de'
        db.add_column(u'people_person', 'involvement_role_de',
                      self.gf('django.db.models.fields.CharField')(u'Default involvement role', unique=False, max_length=255, primary_key=False, db_column=None, blank=True, default='', null=False, editable=True, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Person.involvement_instrument_de'
        db.add_column(u'people_person', 'involvement_instrument_de',
                      self.gf('django.db.models.fields.CharField')(u'Default involvement instrument', unique=False, max_length=255, primary_key=False, db_column=None, blank=True, default='', null=False, editable=True, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Person.involvement_instrument'
        db.add_column(u'people_person', 'involvement_instrument',
                      self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Person.authorship_type'
        db.add_column(u'people_person', 'authorship_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.AuthorshipType'], max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Person.leadership_function_de'
        db.add_column(u'people_person', 'leadership_function_de',
                      self.gf('django.db.models.fields.CharField')(u'Default leadership function', unique=False, max_length=255, primary_key=False, db_column=None, blank=True, default='', null=False, editable=True, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Person.involvement_type'
        db.add_column(u'people_person', 'involvement_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.InvolvementType'], max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Person.leadership_function'
        db.add_column(u'people_person', 'leadership_function',
                      self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Person.involvement_role_en'
        db.add_column(u'people_person', 'involvement_role_en',
                      self.gf('django.db.models.fields.CharField')(u'Default involvement role', unique=False, max_length=255, primary_key=False, db_column=None, blank=True, default='', null=False, editable=True, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Person.involvement_instrument_en'
        db.add_column(u'people_person', 'involvement_instrument_en',
                      self.gf('django.db.models.fields.CharField')(u'Default involvement instrument', unique=False, max_length=255, primary_key=False, db_column=None, blank=True, default='', null=False, editable=True, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Person.involvement_role'
        db.add_column(u'people_person', 'involvement_role',
                      self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Person.leadership_function_en'
        db.add_column(u'people_person', 'leadership_function_en',
                      self.gf('django.db.models.fields.CharField')(u'Default leadership function', unique=False, max_length=255, primary_key=False, db_column=None, blank=True, default='', null=False, editable=True, db_tablespace='', db_index=False),
                      keep_default=False)

    
    
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
        u'people.authorshiptype': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'AuthorshipType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        u'people.involvementtype': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'InvolvementType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        u'people.person': {
            'Meta': {'ordering': "['last_name', 'first_name']", 'object_name': 'Person'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'person_creator'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'person_modifier'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'prefix': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.Prefix']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'draft'", 'max_length': '20', 'blank': 'True'})
        },
        u'people.prefix': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'Prefix'},
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
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
    
    complete_apps = ['people']
