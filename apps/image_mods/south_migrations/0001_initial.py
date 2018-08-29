# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'ImageModification'
        db.create_table('image_mods_imagemodification', south_cleaned_fields((
            ('sysname', self.gf('django.db.models.fields.SlugField')(max_length=255, db_index=True)),
            ('sharpness', self.gf('django.db.models.fields.FloatField')(default=1.0)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('color', self.gf('django.db.models.fields.FloatField')(default=1.0)),
            ('mask', self.gf('filebrowser.fields.FileBrowseField')(null=True, max_length=255, extensions=['.png'], blank=True)),
            ('frame', self.gf('filebrowser.fields.FileBrowseField')(null=True, max_length=255, extensions=['.png'], blank=True)),
            ('brightness', self.gf('django.db.models.fields.FloatField')(default=1.0)),
            ('crop_from', self.gf('django.db.models.fields.CharField')(default='center', max_length=10, blank=True)),
            ('crop', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('height', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('width', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('filters', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('output_format', self.gf('django.db.models.fields.CharField')(default='png', max_length=255)),
            ('quality', self.gf('django.db.models.fields.PositiveIntegerField')(default=70)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contrast', self.gf('django.db.models.fields.FloatField')(default=1.0)),
        )))
        db.send_create_signal('image_mods', ['ImageModification'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'ImageModification'
        db.delete_table('image_mods_imagemodification')
    
    
    models = {
        'image_mods.imagemodification': {
            'Meta': {'object_name': 'ImageModification'},
            'brightness': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'color': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'contrast': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'crop': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'crop_from': ('django.db.models.fields.CharField', [], {'default': "'center'", 'max_length': '10', 'blank': 'True'}),
            'filters': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'frame': ('filebrowser.fields.FileBrowseField', [], {'null': 'True', 'max_length': '255', 'extensions': "['.png']", 'blank': 'True'}),
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mask': ('filebrowser.fields.FileBrowseField', [], {'null': 'True', 'max_length': '255', 'extensions': "['.png']", 'blank': 'True'}),
            'output_format': ('django.db.models.fields.CharField', [], {'default': "'png'", 'max_length': '255'}),
            'quality': ('django.db.models.fields.PositiveIntegerField', [], {'default': '70'}),
            'sharpness': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'sysname': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['image_mods']
