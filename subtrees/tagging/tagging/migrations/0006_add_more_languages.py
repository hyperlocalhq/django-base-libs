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
            if lang_code not in ("en", "de"):
                db.add_column(u'tagging_tag', 'slug_%s' % lang_code,
                              self.gf('django.db.models.fields.SlugField')(default='', max_length=50, blank=True),
                              keep_default=False)
                # Adding field 'Tag.name_pl'
                db.add_column(u'tagging_tag', 'name_%s' % lang_code,
                              self.gf('django.db.models.fields.CharField')(u'name', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=50, db_tablespace='', blank=True, unique=False, db_index=True),
                              keep_default=False)

    
    def backwards(self, orm):
        for lang_code, lang_name in settings.LANGUAGES:
            if lang_code not in ("en", "de"):
                # Deleting field 'Tag.slug_fr'
                db.delete_column(u'tagging_tag', 'slug_%s' % lang_code)

                # Deleting field 'Tag.name_fr'
                db.delete_column(u'tagging_tag', 'name_%s' % lang_code)

    
    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('app_label', 'name')", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'tagging.tag': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'name_de': ('django.db.models.fields.CharField', ["u'name'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '50', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'True'}),
            'name_en': ('django.db.models.fields.CharField', ["u'name'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '50', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'True'}),
            'name_es': ('django.db.models.fields.CharField', ["u'name'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '50', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'True'}),
            'name_fr': ('django.db.models.fields.CharField', ["u'name'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '50', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'True'}),
            'name_it': ('django.db.models.fields.CharField', ["u'name'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '50', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'True'}),
            'name_pl': ('django.db.models.fields.CharField', ["u'name'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '50', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'True'}),
            'name_tr': ('django.db.models.fields.CharField', ["u'name'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '50', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True'}),
            'slug_de': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'slug_en': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'slug_es': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'slug_fr': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'slug_it': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'slug_pl': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'slug_tr': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'tagging.taggeditem': {
            'Meta': {'unique_together': "(('tag', 'content_type', 'object_id'),)", 'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': u"orm['tagging.Tag']"})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['tagging']
