# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'ImageCropping'
        db.create_table('image_mods_imagecropping', south_cleaned_fields((
            ('y2', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('original', self.gf('filebrowser.fields.FileBrowseField')(max_length=255, extensions=['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff'])),
            ('x2', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('y1', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('x1', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        )))
        db.send_create_signal('image_mods', ['ImageCropping'])

        # Adding M2M table for field mods on 'ImageCropping'
        db.create_table('image_mods_imagecropping_mods', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('imagecropping', models.ForeignKey(orm['image_mods.imagecropping'], null=False)),
            ('imagemodification', models.ForeignKey(orm['image_mods.imagemodification'], null=False))
        ))
        db.create_unique('image_mods_imagecropping_mods', ['imagecropping_id', 'imagemodification_id'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'ImageCropping'
        db.delete_table('image_mods_imagecropping')

        # Removing M2M table for field mods on 'ImageCropping'
        db.delete_table('image_mods_imagecropping_mods')
    
    
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
