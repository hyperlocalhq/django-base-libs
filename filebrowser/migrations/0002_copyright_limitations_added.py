# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'FileDescription.copyright_limitations'
        db.add_column('filebrowser_filedescription', 'copyright_limitations', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Deleting field 'FileDescription.copyright_limitations'
        db.delete_column('filebrowser_filedescription', 'copyright_limitations')
    
    
    models = {
        'filebrowser.filedescription': {
            'Meta': {'ordering': "['file_path']", 'object_name': 'FileDescription'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'copyright_limitations': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'description': ('base_libs.models.fields.MultilingualPlainTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'description_de': ('base_libs.models.fields.PlainTextModelField', ["u'Beschreibung'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en': ('base_libs.models.fields.PlainTextModelField', ["u'Beschreibung'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'file_path': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['filebrowser']
