# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Changing field 'FileDescription.title_de'
        db.alter_column(u'filebrowser_filedescription', 'title_de', self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, editable=True, max_length=300, db_tablespace='', unique=False))

        # Changing field 'FileDescription.title_en'
        db.alter_column(u'filebrowser_filedescription', 'title_en', self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, editable=True, max_length=300, db_tablespace='', unique=False))

        # Changing field 'FileDescription.description_en'
        db.alter_column(u'filebrowser_filedescription', 'description_en', self.gf('base_libs.models.fields.PlainTextModelField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, unique=False, db_tablespace=''))

        # Changing field 'FileDescription.description_de'
        db.alter_column(u'filebrowser_filedescription', 'description_de', self.gf('base_libs.models.fields.PlainTextModelField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, unique=False, db_tablespace=''))
    
    
    def backwards(self, orm):
        
        # Changing field 'FileDescription.title_de'
        db.alter_column(u'filebrowser_filedescription', 'title_de', self.gf('django.db.models.fields.CharField')(u'Caption', unique=False, max_length=300, primary_key=False, db_column=None, null=False, editable=True, db_tablespace=''))

        # Changing field 'FileDescription.title_en'
        db.alter_column(u'filebrowser_filedescription', 'title_en', self.gf('django.db.models.fields.CharField')(u'Caption', unique=False, max_length=300, primary_key=False, db_column=None, null=False, editable=True, db_tablespace=''))

        # Changing field 'FileDescription.description_en'
        db.alter_column(u'filebrowser_filedescription', 'description_en', self.gf('base_libs.models.fields.PlainTextModelField')(u'Description (will be used as alt attribute)', rel=None, unique_for_year=None, unique_for_date=None, unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, db_tablespace=''))

        # Changing field 'FileDescription.description_de'
        db.alter_column(u'filebrowser_filedescription', 'description_de', self.gf('base_libs.models.fields.PlainTextModelField')(u'Description (will be used as alt attribute)', rel=None, unique_for_year=None, unique_for_date=None, unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, db_tablespace=''))
    
    
    models = {
        u'filebrowser.filedescription': {
            'Meta': {'ordering': "['file_path']", 'object_name': 'FileDescription'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'copyright_limitations': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'description': ('base_libs.models.fields.MultilingualPlainTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'description_de': ('base_libs.models.fields.PlainTextModelField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en': ('base_libs.models.fields.PlainTextModelField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'file_path': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '300', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '300', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['filebrowser']
