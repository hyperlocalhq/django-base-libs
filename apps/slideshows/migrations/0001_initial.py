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
            ('sysname', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255, db_index=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        )))
        db.send_create_signal('slideshows', ['Slideshow'])

        # Adding model 'Slide'
        db.create_table('slideshows_slide', south_cleaned_fields((
            ('alt_en', self.gf('django.db.models.fields.CharField')(u'Alternative text', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=100, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('alt_de', self.gf('django.db.models.fields.CharField')(u'Alternative text', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=100, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('slideshow', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['slideshows.Slideshow'])),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('path', self.gf('filebrowser.fields.FileBrowseField')(max_length=255, blank=True)),
            ('alt', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=100, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        )))
        db.send_create_signal('slideshows', ['Slide'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Slideshow'
        db.delete_table('slideshows_slideshow')

        # Deleting model 'Slide'
        db.delete_table('slideshows_slide')
    
    
    models = {
        'slideshows.slide': {
            'Meta': {'object_name': 'Slide'},
            'alt': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'alt_de': ('django.db.models.fields.CharField', ["u'Alternative text'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '100', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'alt_en': ('django.db.models.fields.CharField', ["u'Alternative text'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '100', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'path': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255', 'blank': 'True'}),
            'slideshow': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['slideshows.Slideshow']"}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': 'None'})
        },
        'slideshows.slideshow': {
            'Meta': {'object_name': 'Slideshow'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sysname': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['slideshows']
