# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'FilebrowserImage'
        db.create_table(u'cmsplugin_filebrowserimage', south_cleaned_fields((
            (u'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('image', self.gf('filebrowser.fields.FileBrowseField')(max_length=255, extensions=['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff'])),
            ('alt', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('css_class', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('mod', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['image_mods.ImageModification'], null=True, blank=True)),
        )))
        db.send_create_signal(u'filebrowser_image', ['FilebrowserImage'])
    
    
    def backwards(self, orm):
                # Deleting model 'FilebrowserImage'
        db.delete_table(u'cmsplugin_filebrowserimage')

    
    
    models = {
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        u'filebrowser_image.filebrowserimage': {
            'Meta': {'object_name': 'FilebrowserImage', 'db_table': "u'cmsplugin_filebrowserimage'", '_ormbases': ['cms.CMSPlugin']},
            'alt': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'css_class': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']"}),
            'mod': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['image_mods.ImageModification']", 'null': 'True', 'blank': 'True'})
        },
        u'image_mods.imagemodification': {
            'Meta': {'ordering': "('sysname',)", 'object_name': 'ImageModification'},
            'brightness': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'color': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'contrast': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'crop': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'crop_from': ('django.db.models.fields.CharField', [], {'default': "'center'", 'max_length': '10', 'blank': 'True'}),
            'filters': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'frame': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255', 'null': 'True', 'extensions': "['.png']", 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['image_mods.ImageModificationGroup']", 'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mask': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255', 'null': 'True', 'extensions': "['.png']", 'blank': 'True'}),
            'output_format': ('django.db.models.fields.CharField', [], {'default': "'png'", 'max_length': '255'}),
            'quality': ('django.db.models.fields.PositiveIntegerField', [], {'default': '70'}),
            'sharpness': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'sysname': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'image_mods.imagemodificationgroup': {
            'Meta': {'ordering': "('title',)", 'object_name': 'ImageModificationGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['filebrowser_image']
