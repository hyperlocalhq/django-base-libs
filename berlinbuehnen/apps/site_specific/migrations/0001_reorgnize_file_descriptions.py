# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(DataMigration):
    
    def forwards(self, orm):
        counter = 0
        for file_description in orm['filebrowser.filedescription'].objects.exclude(copyright_limitations=""):
            if file_description.author:
                if file_description.description_de:
                    file_description.description_de += '\n' + file_description.author
                else:
                    file_description.description_de = file_description.author
                if file_description.description_en:
                    file_description.description_en += '\n' + file_description.author
                else:
                    file_description.description_en = file_description.author
            file_description.author = file_description.copyright_limitations
            file_description.copyright_limitations = ""
            file_description.save()
            counter += 1
        print "Total changes: {}".format(counter)

    def backwards(self, orm):
        pass

    models = {
        u'filebrowser.filedescription': {
            'Meta': {'ordering': "['file_path']", 'object_name': 'FileDescription'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'copyright_limitations': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'description': ('base_libs.models.fields.MultilingualPlainTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'description_de': ('base_libs.models.fields.PlainTextModelField', ["u'Description (will be used as alt attribute)'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en': ('base_libs.models.fields.PlainTextModelField', ["u'Description (will be used as alt attribute)'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'file_path': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Caption'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '300', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Caption'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '300', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['filebrowser', 'site_specific']
