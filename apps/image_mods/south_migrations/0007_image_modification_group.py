# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'ImageModificationGroup'
        db.create_table('image_mods_imagemodificationgroup', south_cleaned_fields((
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        )))
        db.send_create_signal('image_mods', ['ImageModificationGroup'])

        # Adding field 'ImageModification.group'
        db.add_column('image_mods_imagemodification', 'group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['image_mods.ImageModificationGroup'], null=True, blank=True), keep_default=False)

        # Removing M2M table for field related_mods on 'ImageModification'
        db.delete_table('image_mods_imagemodification_related_mods')
    
    
    def backwards(self, orm):
        
        # Deleting model 'ImageModificationGroup'
        db.delete_table('image_mods_imagemodificationgroup')

        # Deleting field 'ImageModification.group'
        db.delete_column('image_mods_imagemodification', 'group_id')

        # Adding M2M table for field related_mods on 'ImageModification'
        db.create_table('image_mods_imagemodification_related_mods', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_imagemodification', models.ForeignKey(orm['image_mods.imagemodification'], null=False)),
            ('to_imagemodification', models.ForeignKey(orm['image_mods.imagemodification'], null=False))
        ))
        db.create_unique('image_mods_imagemodification_related_mods', ['from_imagemodification_id', 'to_imagemodification_id'])
    
    
    models = {
        'image_mods.imagecropping': {
            'Meta': {'object_name': 'ImageCropping'},
            'bgcolor': ('django.db.models.fields.CharField', [], {'default': "'#ffffff'", 'max_length': '7'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mods': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['image_mods.ImageModification']", 'symmetrical': 'False'}),
            'original': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']"}),
            'x1': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'x2': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'y1': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'y2': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['image_mods.ImageModificationGroup']", 'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mask': ('filebrowser.fields.FileBrowseField', [], {'null': 'True', 'max_length': '255', 'extensions': "['.png']", 'blank': 'True'}),
            'output_format': ('django.db.models.fields.CharField', [], {'default': "'png'", 'max_length': '255'}),
            'quality': ('django.db.models.fields.PositiveIntegerField', [], {'default': '70'}),
            'sharpness': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'sysname': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'image_mods.imagemodificationgroup': {
            'Meta': {'object_name': 'ImageModificationGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['image_mods']
