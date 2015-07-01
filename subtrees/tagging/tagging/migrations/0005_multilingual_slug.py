# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        from django.conf import settings
        
        for lang_code, lang_name in settings.LANGUAGES:
            if lang_code in ("en", "de"):
                # Adding field 'Tag.slug_*'
                db.add_column('tagging_tag', 'slug_%s' % lang_code, self.gf('django.db.models.fields.SlugField')(default='', max_length=50, db_index=True), keep_default=False)

        # Changing field 'Tag.slug'
        db.alter_column('tagging_tag', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True))
    
    
    def backwards(self, orm):
        from django.conf import settings
        
        for lang_code, lang_name in settings.LANGUAGES:
            if lang_code in ("en", "de"):
                # Deleting field 'Tag.slug_*'
                db.delete_column('tagging_tag', 'slug_%s' % lang_code)

        # Changing field 'Tag.slug'
        db.alter_column('tagging_tag', 'slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=50))
    
    
    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('app_label', 'name')", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'tagging.tag': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'name_de': ('django.db.models.fields.CharField', ["u'name'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '50', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'True'}),
            'name_en': ('django.db.models.fields.CharField', ["u'name'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '50', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'slug_de': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'slug_en': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'})
        },
        'tagging.taggeditem': {
            'Meta': {'unique_together': "(('tag', 'content_type', 'object_id'),)", 'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['tagging.Tag']"})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['tagging']
