# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(DataMigration):
    
    def forwards(self, orm):
        im, created = orm.ImageModification.objects.get_or_create(
            sysname="cropping_preview",
            defaults={
                'title': "Cropping Preview",
                'width': 527,
                'height': 527,
            },
            )
    
    def backwards(self, orm):
        orm.ImageModification.objects.filter(
            sysname="cropping_preview",
            ).delete()
    
    models = {
        'image_mods.imagecropping': {
            'Meta': {'object_name': 'ImageCropping'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mods': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['image_mods.ImageModification']", 'symmetrical': 'False'}),
            'original': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']"}),
            'x1': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'x2': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'y1': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'y2': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
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
