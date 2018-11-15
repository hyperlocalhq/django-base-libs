# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from jetson.apps.blocks.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'InfoBlock'
        db.create_table('blocks_infoblock', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('site', models.ForeignKey(orm['sites.Site'], null=True, blank=True)),
            ('sysname', models.SlugField(unique=True, max_length=255)),
            ('title', MultilingualCharField(_('title'), max_length=512, blank=True)),
            ('content', MultilingualTextField(_('content'))),
            ('title_de', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=512, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('title_en', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=512, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('content_de', ExtendedTextField(u'content', unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, unique_for_year=None, rel=None, blank=False, null=False, unique_for_date=None, db_tablespace='', db_index=False)),
            ('content_de_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('content_en', ExtendedTextField(u'content', unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, unique_for_year=None, rel=None, blank=False, null=False, unique_for_date=None, db_tablespace='', db_index=False)),
            ('content_en_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('content_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
        )))
        db.send_create_signal('blocks', ['InfoBlock'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'InfoBlock'
        db.delete_table('blocks_infoblock')
        
    
    
    models = {
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'db_table': "'django_site'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'blocks.infoblock': {
            'Meta': {'ordering': "['sysname']"},
            'content': ('MultilingualTextField', ["_('content')"], {}),
            'content_de': ('ExtendedTextField', ["u'content'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'False', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'content_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'content_en': ('ExtendedTextField', ["u'content'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'False', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'content_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'content_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'site': ('models.ForeignKey', ["orm['sites.Site']"], {'null': 'True', 'blank': 'True'}),
            'sysname': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'title': ('MultilingualCharField', ["_('title')"], {'max_length': '512', 'blank': 'True'}),
            'title_de': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '512', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '512', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['blocks']
