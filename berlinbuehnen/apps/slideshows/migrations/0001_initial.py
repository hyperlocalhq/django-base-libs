# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Slideshow'
        db.create_table(u'slideshows_slideshow', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sysname', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
        )))
        db.send_create_signal(u'slideshows', ['Slideshow'])

        # Adding model 'Slide'
        db.create_table(u'slideshows_slide', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slideshow', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['slideshows.Slideshow'])),
            ('path', self.gf('filebrowser.fields.FileBrowseField')(directory='slideshows/', max_length=255, blank=True)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('alt', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=100, null=True, blank=True)),
            ('title', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True)),
            ('subtitle', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True)),
            ('credits', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True, blank=True)),
            ('highlight', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('subtitle_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Subtitle', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('subtitle_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('subtitle_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Subtitle', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('subtitle_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('title_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Title', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('title_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('title_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Title', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('title_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('credits_de', self.gf('django.db.models.fields.CharField')(u'Photo credits', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('credits_en', self.gf('django.db.models.fields.CharField')(u'Photo credits', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('alt_de', self.gf('django.db.models.fields.CharField')(u'Alternative text', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=100, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('alt_en', self.gf('django.db.models.fields.CharField')(u'Alternative text', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=100, db_tablespace='', blank=True, unique=False, db_index=False)),
        )))
        db.send_create_signal(u'slideshows', ['Slide'])
    
    
    def backwards(self, orm):
                # Deleting model 'Slideshow'
        db.delete_table(u'slideshows_slideshow')

        # Deleting model 'Slide'
        db.delete_table(u'slideshows_slide')

    
    
    models = {
        u'slideshows.slide': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'Slide'},
            'alt': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'alt_de': ('django.db.models.fields.CharField', ["u'Alternative text'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '100', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'alt_en': ('django.db.models.fields.CharField', ["u'Alternative text'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '100', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'credits': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'credits_de': ('django.db.models.fields.CharField', ["u'Photo credits'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'credits_en': ('django.db.models.fields.CharField', ["u'Photo credits'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'highlight': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'path': ('filebrowser.fields.FileBrowseField', [], {'directory': "'slideshows/'", 'max_length': '255', 'blank': 'True'}),
            'slideshow': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': u"orm['slideshows.Slideshow']"}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'subtitle': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'subtitle_de': ('base_libs.models.fields.ExtendedTextField', ["u'Subtitle'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'subtitle_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'subtitle_en': ('base_libs.models.fields.ExtendedTextField', ["u'Subtitle'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'subtitle_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'title': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'title_de': ('base_libs.models.fields.ExtendedTextField', ["u'Title'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'title_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'title_en': ('base_libs.models.fields.ExtendedTextField', ["u'Title'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'title_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'})
        },
        u'slideshows.slideshow': {
            'Meta': {'ordering': "['sysname']", 'object_name': 'Slideshow'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sysname': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['slideshows']
