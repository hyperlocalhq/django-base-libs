# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'Slide.title'
        db.add_column('slideshows_slide', 'title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'Slide.subtitle'
        db.add_column('slideshows_slide', 'subtitle', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'Slide.credits'
        db.add_column('slideshows_slide', 'credits', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'Slide.subtitle_de'
        db.add_column('slideshows_slide', 'subtitle_de', self.gf('django.db.models.fields.CharField')(u'Subtitle', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False), keep_default=False)

        # Adding field 'Slide.title_de'
        db.add_column('slideshows_slide', 'title_de', self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False), keep_default=False)

        # Adding field 'Slide.credits_de'
        db.add_column('slideshows_slide', 'credits_de', self.gf('django.db.models.fields.CharField')(u'Credits', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False), keep_default=False)

        # Changing field 'Slide.path'
        db.alter_column('slideshows_slide', 'path', self.gf('filebrowser.fields.FileBrowseField')(directory='slideshows/', max_length=255))
    
    
    def backwards(self, orm):
        
        # Deleting field 'Slide.title'
        db.delete_column('slideshows_slide', 'title')

        # Deleting field 'Slide.subtitle'
        db.delete_column('slideshows_slide', 'subtitle')

        # Deleting field 'Slide.credits'
        db.delete_column('slideshows_slide', 'credits')

        # Deleting field 'Slide.subtitle_de'
        db.delete_column('slideshows_slide', 'subtitle_de')

        # Deleting field 'Slide.title_de'
        db.delete_column('slideshows_slide', 'title_de')

        # Deleting field 'Slide.credits_de'
        db.delete_column('slideshows_slide', 'credits_de')

        # Changing field 'Slide.path'
        db.alter_column('slideshows_slide', 'path', self.gf('filebrowser.fields.FileBrowseField')(max_length=255))
    
    
    models = {
        'slideshows.slide': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'Slide'},
            'alt': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'alt_de': ('django.db.models.fields.CharField', ["u'Alternative text'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '100', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'credits': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'credits_de': ('django.db.models.fields.CharField', ["u'Credits'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'path': ('filebrowser.fields.FileBrowseField', [], {'directory': "'slideshows/'", 'max_length': '255', 'blank': 'True'}),
            'slideshow': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['slideshows.Slideshow']"}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'subtitle': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subtitle_de': ('django.db.models.fields.CharField', ["u'Subtitle'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        'slideshows.slideshow': {
            'Meta': {'ordering': "['sysname']", 'object_name': 'Slideshow'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sysname': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['slideshows']
