# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'NavigationLink.lft'
        db.add_column('navigation_navigationlink', 'lft', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True), keep_default=False)

        # Adding field 'NavigationLink.rght'
        db.add_column('navigation_navigationlink', 'rght', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True), keep_default=False)

        # Adding field 'NavigationLink.tree_id'
        db.add_column('navigation_navigationlink', 'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True), keep_default=False)

        # Adding field 'NavigationLink.level'
        db.add_column('navigation_navigationlink', 'level', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True), keep_default=False)

        # Changing field 'NavigationLink.is_shown_for_users'
        db.alter_column('navigation_navigationlink', 'is_shown_for_users', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'NavigationLink.site'
        db.alter_column('navigation_navigationlink', 'site_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'], null=True))

        # Changing field 'NavigationLink.sort_order'
        db.alter_column('navigation_navigationlink', 'sort_order', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'NavigationLink.description_de'
        db.alter_column('navigation_navigationlink', 'description_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Beschreibung', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, unique=False, db_tablespace=''))

        # Changing field 'NavigationLink.is_shown_for_visitors'
        db.alter_column('navigation_navigationlink', 'is_shown_for_visitors', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'NavigationLink.is_promoted'
        db.alter_column('navigation_navigationlink', 'is_promoted', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'NavigationLink.title'
        db.alter_column('navigation_navigationlink', 'title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True))

        # Changing field 'NavigationLink.is_group_name_shown'
        db.alter_column('navigation_navigationlink', 'is_group_name_shown', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'NavigationLink.description'
        db.alter_column('navigation_navigationlink', 'description', self.gf('base_libs.models.fields.MultilingualTextField')(null=True))

        # Changing field 'NavigationLink.parent'
        db.alter_column('navigation_navigationlink', 'parent_id', self.gf('mptt.fields.TreeForeignKey')(null=True, to=orm['navigation.NavigationLink']))

        # Changing field 'NavigationLink.related_urls'
        db.alter_column('navigation_navigationlink', 'related_urls', self.gf('base_libs.models.fields.PlainTextModelField')())

        # Changing field 'NavigationLink.is_group'
        db.alter_column('navigation_navigationlink', 'is_group', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'NavigationLink.description_en'
        db.alter_column('navigation_navigationlink', 'description_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Beschreibung', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, unique=False, db_tablespace=''))

        # Changing field 'NavigationLink.content_type'
        db.alter_column('navigation_navigationlink', 'content_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True))

        # Changing field 'NavigationLink.is_login_required'
        db.alter_column('navigation_navigationlink', 'is_login_required', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'NavigationLink.path'
        db.alter_column('navigation_navigationlink', 'path', self.gf('django.db.models.fields.CharField')(max_length=8192, null=True))

        # Changing field 'NavigationLink.link_url'
        db.alter_column('navigation_navigationlink', 'link_url', self.gf('django.db.models.fields.CharField')(max_length=255))
    
    
    def backwards(self, orm):
        pass
    
    
    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('app_label', 'name')", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'navigation.navigationlink': {
            'Meta': {'ordering': "['path', 'sort_order']", 'object_name': 'NavigationLink'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'description': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'description_de': ('base_libs.models.fields.ExtendedTextField', ["u'Beschreibung'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('base_libs.models.fields.ExtendedTextField', ["u'Beschreibung'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_group': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_group_name_shown': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_promoted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_shown_for_users': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_shown_for_visitors': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'link_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'child_set'", 'null': 'True', 'to': "orm['navigation.NavigationLink']"}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '8192', 'null': 'True'}),
            'related_urls': ('base_libs.models.fields.PlainTextModelField', [], {'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']", 'null': 'True', 'blank': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'sysname': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['navigation']
