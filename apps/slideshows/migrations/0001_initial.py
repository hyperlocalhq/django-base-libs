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
        db.create_table('slideshows_slideshow', south_cleaned_fields((
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sysname', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255, db_index=True)),
        )))
        db.send_create_signal('slideshows', ['Slideshow'])

        # Adding model 'Slide'
        db.create_table('slideshows_slide', south_cleaned_fields((
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slideshow', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['slideshows.Slideshow'])),
            ('path', self.gf('filebrowser.fields.FileBrowseField')(directory='slideshows/', max_length=255, blank=True)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('alt', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=100, null=True, blank=True)),
            ('title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True, blank=True)),
            ('title2', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True, blank=True)),
            ('title3', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True, blank=True)),
            ('subtitle', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True, blank=True)),
            ('credits', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True, blank=True)),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('subtitle_de', self.gf('django.db.models.fields.CharField')(u'Subtitle', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('subtitle_en', self.gf('django.db.models.fields.CharField')(u'Subtitle', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('title_de', self.gf('django.db.models.fields.CharField')(u'Title Line 1', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('title_en', self.gf('django.db.models.fields.CharField')(u'Title Line 1', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('credits_de', self.gf('django.db.models.fields.CharField')(u'Photo credits', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('credits_en', self.gf('django.db.models.fields.CharField')(u'Photo credits', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('title2_de', self.gf('django.db.models.fields.CharField')(u'Title Line 2', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('title2_en', self.gf('django.db.models.fields.CharField')(u'Title Line 2', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('title3_de', self.gf('django.db.models.fields.CharField')(u'Title Line 3', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('title3_en', self.gf('django.db.models.fields.CharField')(u'Title Line 3', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('alt_de', self.gf('django.db.models.fields.CharField')(u'Alternative text', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=100, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('alt_en', self.gf('django.db.models.fields.CharField')(u'Alternative text', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=100, db_tablespace='', blank=True, unique=False, db_index=False)),
        )))
        db.send_create_signal('slideshows', ['Slide'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Slideshow'
        db.delete_table('slideshows_slideshow')

        # Deleting model 'Slide'
        db.delete_table('slideshows_slide')
    
    
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
            'subtitle': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subtitle_de': ('django.db.models.fields.CharField', ["u'Subtitle'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'subtitle_en': ('django.db.models.fields.CharField', ["u'Subtitle'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title2': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title2_de': ('django.db.models.fields.CharField', ["u'Title Line 2'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title2_en': ('django.db.models.fields.CharField', ["u'Title Line 2'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title3': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title3_de': ('django.db.models.fields.CharField', ["u'Title Line 3'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title3_en': ('django.db.models.fields.CharField', ["u'Title Line 3'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title Line 1'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title Line 1'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        'slideshows.slideshow': {
            'Meta': {'ordering': "['sysname']", 'object_name': 'Slideshow'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sysname': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['slideshows']
