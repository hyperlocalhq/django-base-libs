# -*- coding: UTF-8 -*-

from django.db import models

from south.db import db

from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

from ccb.apps.external_services.models import *
from ccb.apps.articles.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'ServiceActionLog'
        db.create_table('external_services_serviceactionlog', south_cleaned_fields((
            ('id', orm['external_services.serviceactionlog:id']),
            ('creation_date', orm['external_services.serviceactionlog:creation_date']),
            ('service', orm['external_services.serviceactionlog:service']),
            ('request', orm['external_services.serviceactionlog:request']),
            ('response', orm['external_services.serviceactionlog:response']),
            ('response_code', orm['external_services.serviceactionlog:response_code']),
        )))
        db.send_create_signal('external_services', ['ServiceActionLog'])
    
    def backwards(self, orm):
        
        # Deleting model 'ServiceActionLog'
        db.delete_table('external_services_serviceactionlog')
        
    
    
    models = {
        'articles.articlecontentprovider': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'url': ('URLField', ['_("URL")'], {'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'external_services.articleimportsource': {
            'Meta': {'db_table': "'external_services_ais'"},
            'are_excerpts': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'content_provider': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.ArticleContentProvider']", 'null': 'True', 'blank': 'True'}),
            'default_creative_sectors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['structure.Term']", 'null': 'True', 'db_column': "'default_cs'", 'blank': 'True'}),
            'default_sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'null': 'True', 'blank': 'True'}),
            'default_status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'service_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['external_services.Service']", 'unique': 'True', 'primary_key': 'True'})
        },
        'external_services.objectmapper': {
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'related_name': 'None', 'null': 'False', 'blank': 'False'}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('models.CharField', ["u'Related object'"], {'max_length': '255', 'null': 'False', 'blank': 'False'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['external_services.Service']"})
        },
        'external_services.service': {
            'api_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'sysname': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'})
        },
        'external_services.serviceactionlog': {
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'request': ('PlainTextModelField', ['_("Request")'], {'blank': 'True'}),
            'response': ('PlainTextModelField', ['_("Response")'], {'blank': 'True'}),
            'response_code': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['external_services.Service']"})
        },
        'sites.site': {
            'Meta': {'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'structure.term': {
            'body': ('MultilingualTextField', ["_('body')"], {'blank': 'True'}),
            'body_de': ('ExtendedTextField', ["u'body'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'body_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'body_en': ('ExtendedTextField', ["u'body'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'body_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'body_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('FileBrowseField', ["_('Image')"], {'max_length': '255', 'extensions': "['.jpg','.jpeg','.gif','.png','.tif','.tiff']", 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'child_set'", 'blank': 'True', 'null': 'True', 'to': "orm['structure.Term']"}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '8192', 'null': 'True'}),
            'path_search': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'sysname': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'title': ('MultilingualCharField', ["_('title')"], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'vocabulary': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structure.Vocabulary']"})
        },
        'structure.vocabulary': {
            'body': ('MultilingualTextField', ["_('body')"], {'blank': 'True'}),
            'body_de': ('ExtendedTextField', ["u'body'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'body_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'body_en': ('ExtendedTextField', ["u'body'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'body_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'body_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'hierarchy': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('FileBrowseField', ["_('Image')"], {'max_length': '255', 'extensions': "['.jpg','.jpeg','.gif','.png','.tif','.tiff']", 'blank': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sysname': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'title': ('MultilingualCharField', ["_('title')"], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['external_services']
