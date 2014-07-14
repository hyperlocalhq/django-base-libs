# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from ccb.apps.resources.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Document.description_markup_type'
        db.add_column('resources_document', 'description_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False))
        
        # Adding field 'Document.description_en_markup_type'
        db.add_column('resources_document', 'description_en_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False))
        
        # Adding field 'Document.description_en'
        db.add_column('resources_document', 'description_en', ExtendedTextField(u'Description', unique_for_month=None, unique=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, null=False, unique_for_date=None, db_tablespace='', db_index=False))
        
        # Adding field 'Document.title_en'
        db.add_column('resources_document', 'title_en', models.CharField(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False))
        
        # Adding field 'Document.description_de_markup_type'
        db.add_column('resources_document', 'description_de_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False))
        
        # Changing field 'Document.title_de'
        db.alter_column('resources_document', 'title_de', models.CharField(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False))
        
        # Changing field 'Document.description_de'
        db.alter_column('resources_document', 'description_de', ExtendedTextField(u'Description', unique_for_month=None, unique=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, null=False, unique_for_date=None, db_tablespace='', db_index=False))
        
        # Changing field 'Document.description'
        db.alter_column('resources_document', 'description', MultilingualTextField(_("Description"), blank=True))
        
        # Changing field 'Document.title'
        db.alter_column('resources_document', 'title', MultilingualCharField(_("Title"), max_length=255))
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Document.description_markup_type'
        db.delete_column('resources_document', 'description_markup_type')
        
        # Deleting field 'Document.description_en_markup_type'
        db.delete_column('resources_document', 'description_en_markup_type')
        
        # Deleting field 'Document.description_en'
        db.delete_column('resources_document', 'description_en')
        
        # Deleting field 'Document.title_en'
        db.delete_column('resources_document', 'title_en')
        
        # Deleting field 'Document.description_de_markup_type'
        db.delete_column('resources_document', 'description_de_markup_type')
        
        # Changing field 'Document.title_de'
        db.alter_column('resources_document', 'title_de', models.CharField(_("Title (German)"), max_length=255, blank=True))
        
        # Changing field 'Document.description_de'
        db.alter_column('resources_document', 'description_de', models.TextField(_("Description (German)"), blank=True))
        
        # Changing field 'Document.description'
        db.alter_column('resources_document', 'description', models.TextField(_("Description (English)"), blank=True))
        
        # Changing field 'Document.title'
        db.alter_column('resources_document', 'title', models.CharField(_("Title (English)"), max_length=255))
        
    
    
    models = {
        'people.person': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'structure.contextcategory': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'resources.document': {
            'authors': ('models.ManyToManyField', ["orm['people.Person']"], {'related_name': '"author_documents"', 'blank': 'True'}),
            'authors_plain': ('PlainTextModelField', ['_("External authors")'], {'max_length': '255', 'blank': 'True'}),
            'context_categories': ('models.ManyToManyField', ["orm['structure.ContextCategory']"], {'limit_choices_to': "{'is_applied4document':True}", 'blank': 'True'}),
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'editable': 'False'}),
            'creative_sectors': ('models.ManyToManyField', ["orm['structure.Term']"], {'limit_choices_to': "{'vocabulary__sysname':'categories_creativesectors'}", 'related_name': '"creative_industry_documents"', 'blank': 'True'}),
            'description': ('MultilingualTextField', ['_("Description")'], {'blank': 'True'}),
            'description_de': ('ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'document_file': ('FileBrowseField', ["_('Document file')"], {'max_length': '255', 'blank': 'True'}),
            'document_type': ('models.ForeignKey', ["orm['structure.Term']"], {'limit_choices_to': 'models.Q(vocabulary__sysname=\'basics_object_types\',path_search__contains=ObjectTypeFilter("document"))&~models.Q(models.Q(sysname="document"))', 'related_name': '"type_documents"'}),
            'file_size': ('models.PositiveIntegerField', ['_("File size (MB)")'], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'image': ('FileBrowseField', ["_('Image')"], {'extensions': "['.jpg','.jpeg','.gif','.png','.tif','.tiff']", 'max_length': '255', 'directory': '"/%s/"%URL_ID_DOCUMENTS', 'blank': 'True'}),
            'isbn10': ('models.CharField', ['_("ISBN-10")'], {'max_length': '13', 'blank': 'True'}),
            'isbn13': ('models.CharField', ['_("ISBN-13")'], {'max_length': '17', 'blank': 'True'}),
            'languages': ('models.ManyToManyField', ["orm['i18n.Language']"], {'limit_choices_to': "{'display':True}", 'blank': 'True'}),
            'medium': ('models.ForeignKey', ["orm['structure.Term']"], {'limit_choices_to': "{'vocabulary__sysname':'basics_media'}", 'related_name': '"medium_documents"', 'null': 'True', 'blank': 'True'}),
            'modified_date': ('models.DateTimeField', ['_("modified date")'], {'null': 'True', 'editable': 'False'}),
            'pages': ('models.PositiveIntegerField', ['_("Pages")'], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'playing_time': ('models.TimeField', ['_("Playing time")'], {'null': 'True', 'blank': 'True'}),
            'published_dd': ('models.SmallIntegerField', ['_("Day of Publishing")'], {'null': 'True', 'blank': 'True'}),
            'published_mm': ('models.SmallIntegerField', ['_("Month of Publishing")'], {'null': 'True', 'blank': 'True'}),
            'published_yyyy': ('models.IntegerField', ['_("Year of Publishing")'], {'null': 'True', 'blank': 'True'}),
            'publisher': ('models.ForeignKey', ["orm['institutions.Institution']"], {'null': 'True', 'blank': 'True'}),
            'slug': ('models.CharField', ['_("Slug")'], {'max_length': '255'}),
            'status': ('models.ForeignKey', ["orm['structure.Term']"], {'limit_choices_to': "{'vocabulary__sysname':'basics_object_statuses'}", 'related_name': '"status_documents"', 'default': 'DefaultObjectStatus("draft")', 'blank': 'True', 'null': 'True'}),
            'title': ('MultilingualCharField', ['_("Title")'], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'url_link': ('URLField', ['_("URL")'], {'blank': 'True'})
        },
        'structure.term': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'institutions.institution': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'i18n.language': {
            'Meta': {'ordering': "XFieldList(['sort_order','name_'])"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['resources']
