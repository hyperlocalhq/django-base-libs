# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'MenuBlock'
        db.create_table(u'mega_menu_menublock', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sysname', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('left_column', self.gf('base_libs.models.fields.ExtendedTextField')(blank=True)),
            ('center_column', self.gf('base_libs.models.fields.ExtendedTextField')(blank=True)),
            ('right_column_headline', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('right_column_description', self.gf('base_libs.models.fields.ExtendedTextField')(blank=True)),
            ('right_column_image', self.gf('filebrowser.fields.FileBrowseField')(directory='menu/', max_length=255, extensions=['.jpg', '.jpeg', '.gif', '.png'], blank=True)),
            ('right_column_link', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('left_column_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('right_column_description_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('center_column_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
        )))
        db.send_create_signal(u'mega_menu', ['MenuBlock'])
    
    
    def backwards(self, orm):
                # Deleting model 'MenuBlock'
        db.delete_table(u'mega_menu_menublock')

    
    
    models = {
        u'mega_menu.menublock': {
            'Meta': {'object_name': 'MenuBlock'},
            'center_column': ('base_libs.models.fields.ExtendedTextField', [], {'blank': 'True'}),
            'center_column_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'left_column': ('base_libs.models.fields.ExtendedTextField', [], {'blank': 'True'}),
            'left_column_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'right_column_description': ('base_libs.models.fields.ExtendedTextField', [], {'blank': 'True'}),
            'right_column_description_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'right_column_headline': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'right_column_image': ('filebrowser.fields.FileBrowseField', [], {'directory': "'menu/'", 'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png']", 'blank': 'True'}),
            'right_column_link': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'sysname': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['mega_menu']
