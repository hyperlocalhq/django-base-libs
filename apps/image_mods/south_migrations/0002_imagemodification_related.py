# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding M2M table for field related_mods on 'ImageModification'
        db.create_table('image_mods_imagemodification_related_mods', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_imagemodification', models.ForeignKey(orm['image_mods.imagemodification'], null=False)),
            ('to_imagemodification', models.ForeignKey(orm['image_mods.imagemodification'], null=False))
        ))
        db.create_unique('image_mods_imagemodification_related_mods', ['from_imagemodification_id', 'to_imagemodification_id'])
    
    
    def backwards(self, orm):
        
        # Removing M2M table for field related_mods on 'ImageModification'
        db.delete_table('image_mods_imagemodification_related_mods')
    
    
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
            'related_mods': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_mods_rel_+'", 'blank': 'True', 'to': "orm['image_mods.ImageModification']"}),
            'sharpness': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'sysname': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['image_mods']
