# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.conf import settings
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Changing field 'FileDescription.title'
        db.alter_column('filebrowser_filedescription', 'title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=300, null=True))

        # Changing field 'FileDescription.author'
        db.alter_column('filebrowser_filedescription', 'author', self.gf('django.db.models.fields.CharField')(max_length=300))

        for lang_code, lang_name in settings.LANGUAGES:
            try:
                # Changing field 'FileDescription.title_*'
                db.alter_column('filebrowser_filedescription', 'title_%s' % lang_code, self.gf('django.db.models.fields.CharField')(u'Caption', null=False, primary_key=False, db_column=None, editable=True, max_length=300, db_tablespace='', unique=False))

                # Changing field 'FileDescription.description_*'
                db.alter_column('filebrowser_filedescription', 'description_%s' % lang_code, self.gf('base_libs.models.fields.PlainTextModelField')(u'Description (will be used as alt attribute)', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, unique=False, db_tablespace=''))
            except Exception as e:
                pass

        # Changing field 'FileDescription.copyright_limitations'
        db.alter_column('filebrowser_filedescription', 'copyright_limitations', self.gf('django.db.models.fields.CharField')(max_length=300))


    
    def backwards(self, orm):
        
        # Changing field 'FileDescription.title'
        db.alter_column('filebrowser_filedescription', 'title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True))

        # Changing field 'FileDescription.author'
        db.alter_column('filebrowser_filedescription', 'author', self.gf('django.db.models.fields.CharField')(max_length=255))

        for lang_code, lang_name in settings.LANGUAGES:
            # Changing field 'FileDescription.title_*'
            db.alter_column('filebrowser_filedescription', 'title_%s' % lang_code, self.gf('django.db.models.fields.CharField')(u'Title', unique=False, max_length=255, primary_key=False, db_column=None, null=False, editable=True, db_tablespace=''))

            # Changing field 'FileDescription.description_*'
            db.alter_column('filebrowser_filedescription', 'description_%s' % lang_code, self.gf('base_libs.models.fields.PlainTextModelField')(u'Beschreibung', rel=None, unique_for_year=None, unique_for_date=None, unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, db_tablespace=''))

        # Changing field 'FileDescription.copyright_limitations'
        db.alter_column('filebrowser_filedescription', 'copyright_limitations', self.gf('django.db.models.fields.CharField')(max_length=255))


    
    models = {
        'filebrowser.filedescription': {
            'Meta': {'ordering': "['file_path']", 'object_name': 'FileDescription'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'copyright_limitations': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'description': ('base_libs.models.fields.MultilingualPlainTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'description_de': ('base_libs.models.fields.PlainTextModelField', ["u'Description (will be used as alt attribute)'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en': ('base_libs.models.fields.PlainTextModelField', ["u'Description (will be used as alt attribute)'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'file_path': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Caption'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '300', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Caption'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '300', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['filebrowser']
