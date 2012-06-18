# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Deleting field 'Slide.title2_en'
        db.delete_column('slideshows_slide', 'title2_en')

        # Deleting field 'Slide.title3_de'
        db.delete_column('slideshows_slide', 'title3_de')

        # Deleting field 'Slide.title2_de'
        db.delete_column('slideshows_slide', 'title2_de')

        # Deleting field 'Slide.title2'
        db.delete_column('slideshows_slide', 'title2')

        # Deleting field 'Slide.title3'
        db.delete_column('slideshows_slide', 'title3')

        # Deleting field 'Slide.title3_en'
        db.delete_column('slideshows_slide', 'title3_en')

        # Adding field 'Slide.subtitle_de_markup_type'
        db.add_column('slideshows_slide', 'subtitle_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Slide.subtitle_en_markup_type'
        db.add_column('slideshows_slide', 'subtitle_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Slide.subtitle_markup_type'
        db.add_column('slideshows_slide', 'subtitle_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Slide.title_de_markup_type'
        db.add_column('slideshows_slide', 'title_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Slide.title_en_markup_type'
        db.add_column('slideshows_slide', 'title_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Slide.title_markup_type'
        db.add_column('slideshows_slide', 'title_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Changing field 'Slide.title_de'
        db.alter_column('slideshows_slide', 'title_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Titel', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, unique=False, db_tablespace=''))

        # Changing field 'Slide.subtitle'
        db.alter_column('slideshows_slide', 'subtitle', self.gf('base_libs.models.fields.MultilingualTextField')(null=True))

        # Changing field 'Slide.title'
        db.alter_column('slideshows_slide', 'title', self.gf('base_libs.models.fields.MultilingualTextField')(null=True))

        # Changing field 'Slide.title_en'
        db.alter_column('slideshows_slide', 'title_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Titel', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, unique=False, db_tablespace=''))

        # Changing field 'Slide.subtitle_de'
        db.alter_column('slideshows_slide', 'subtitle_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Untertitel', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, unique=False, db_tablespace=''))

        # Changing field 'Slide.subtitle_en'
        db.alter_column('slideshows_slide', 'subtitle_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Untertitel', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, unique=False, db_tablespace=''))
    
    
    def backwards(self, orm):
        
        # Adding field 'Slide.title2_en'
        db.add_column('slideshows_slide', 'title2_en', self.gf('django.db.models.fields.CharField')(u'Title Line 2', unique=False, max_length=255, primary_key=False, db_column=None, blank=True, default='', null=False, editable=True, db_tablespace='', db_index=False), keep_default=False)

        # Adding field 'Slide.title3_de'
        db.add_column('slideshows_slide', 'title3_de', self.gf('django.db.models.fields.CharField')(u'Title Line 3', unique=False, max_length=255, primary_key=False, db_column=None, blank=True, default='', null=False, editable=True, db_tablespace='', db_index=False), keep_default=False)

        # Adding field 'Slide.title2_de'
        db.add_column('slideshows_slide', 'title2_de', self.gf('django.db.models.fields.CharField')(u'Title Line 2', unique=False, max_length=255, primary_key=False, db_column=None, blank=True, default='', null=False, editable=True, db_tablespace='', db_index=False), keep_default=False)

        # Adding field 'Slide.title2'
        db.add_column('slideshows_slide', 'title2', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'Slide.title3'
        db.add_column('slideshows_slide', 'title3', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'Slide.title3_en'
        db.add_column('slideshows_slide', 'title3_en', self.gf('django.db.models.fields.CharField')(u'Title Line 3', unique=False, max_length=255, primary_key=False, db_column=None, blank=True, default='', null=False, editable=True, db_tablespace='', db_index=False), keep_default=False)

        # Deleting field 'Slide.subtitle_de_markup_type'
        db.delete_column('slideshows_slide', 'subtitle_de_markup_type')

        # Deleting field 'Slide.subtitle_en_markup_type'
        db.delete_column('slideshows_slide', 'subtitle_en_markup_type')

        # Deleting field 'Slide.subtitle_markup_type'
        db.delete_column('slideshows_slide', 'subtitle_markup_type')

        # Deleting field 'Slide.title_de_markup_type'
        db.delete_column('slideshows_slide', 'title_de_markup_type')

        # Deleting field 'Slide.title_en_markup_type'
        db.delete_column('slideshows_slide', 'title_en_markup_type')

        # Deleting field 'Slide.title_markup_type'
        db.delete_column('slideshows_slide', 'title_markup_type')

        # Changing field 'Slide.title_de'
        db.alter_column('slideshows_slide', 'title_de', self.gf('django.db.models.fields.CharField')(u'Title Line 1', unique=False, max_length=255, primary_key=False, db_column=None, null=False, editable=True, db_tablespace=''))

        # Changing field 'Slide.subtitle'
        db.alter_column('slideshows_slide', 'subtitle', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True))

        # Changing field 'Slide.title'
        db.alter_column('slideshows_slide', 'title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True))

        # Changing field 'Slide.title_en'
        db.alter_column('slideshows_slide', 'title_en', self.gf('django.db.models.fields.CharField')(u'Title Line 1', unique=False, max_length=255, primary_key=False, db_column=None, null=False, editable=True, db_tablespace=''))

        # Changing field 'Slide.subtitle_de'
        db.alter_column('slideshows_slide', 'subtitle_de', self.gf('django.db.models.fields.CharField')(u'Subtitle', unique=False, max_length=255, primary_key=False, db_column=None, null=False, editable=True, db_tablespace=''))

        # Changing field 'Slide.subtitle_en'
        db.alter_column('slideshows_slide', 'subtitle_en', self.gf('django.db.models.fields.CharField')(u'Subtitle', unique=False, max_length=255, primary_key=False, db_column=None, null=False, editable=True, db_tablespace=''))
    
    
    models = {
        'slideshows.slide': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'Slide'},
            'alt': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'alt_de': ('django.db.models.fields.CharField', ["u'Alternative text'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '100', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'alt_en': ('django.db.models.fields.CharField', ["u'Alternative text'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '100', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'credits': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'credits_de': ('django.db.models.fields.CharField', ["u'Photo credits'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'credits_en': ('django.db.models.fields.CharField', ["u'Photo credits'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'path': ('filebrowser.fields.FileBrowseField', [], {'directory': "'slideshows/'", 'max_length': '255', 'blank': 'True'}),
            'slideshow': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['slideshows.Slideshow']"}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'subtitle': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'subtitle_de': ('base_libs.models.fields.ExtendedTextField', ["u'Untertitel'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'subtitle_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'subtitle_en': ('base_libs.models.fields.ExtendedTextField', ["u'Untertitel'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'subtitle_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'subtitle_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'title': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'title_de': ('base_libs.models.fields.ExtendedTextField', ["u'Titel'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'title_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'title_en': ('base_libs.models.fields.ExtendedTextField', ["u'Titel'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'title_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'title_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'})
        },
        'slideshows.slideshow': {
            'Meta': {'ordering': "['sysname']", 'object_name': 'Slideshow'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sysname': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['slideshows']
