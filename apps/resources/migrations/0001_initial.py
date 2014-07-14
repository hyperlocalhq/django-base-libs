# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from ccb.apps.resources.models import *
from base_libs.utils.misc import south_clean_multilingual_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Document'
        db.create_table('resources_document', (
            ('id', models.AutoField(primary_key=True)),
            ('creation_date', models.DateTimeField(_("creation date"), editable=False)),
            ('modified_date', models.DateTimeField(_("modified date"), null=True, editable=False)),
            ('title', models.CharField(_("Title (English)"), max_length=255)),
            ('title_de', models.CharField(_("Title (German)"), max_length=255, blank=True)),
            ('slug', models.CharField(_("Slug"), max_length=255)),
            ('description', models.TextField(_("Description (English)"), blank=True)),
            ('description_de', models.TextField(_("Description (German)"), blank=True)),
            ('document_type', models.ForeignKey(orm['structure.Term'], limit_choices_to=models.Q(vocabulary__sysname='basics_object_types',path_search__contains=ObjectTypeFilter("document"))&~models.Q(models.Q(sysname="document")), related_name="type_documents")),
            ('medium', models.ForeignKey(orm['structure.Term'], limit_choices_to={'vocabulary__sysname':'basics_media'}, related_name="medium_documents", null=True, blank=True)),
            ('url_link', URLField(_("URL"), blank=True)),
            ('document_file', FileBrowseField(_('Document file'), max_length=255, blank=True)),
            ('authors_plain', PlainTextModelField(_("External authors"), max_length=255, blank=True)),
            ('publisher', models.ForeignKey(orm['institutions.Institution'], null=True, blank=True)),
            ('published_yyyy', models.IntegerField(_("Year of Publishing"), null=True, blank=True)),
            ('published_mm', models.SmallIntegerField(_("Month of Publishing"), null=True, blank=True)),
            ('published_dd', models.SmallIntegerField(_("Day of Publishing"), null=True, blank=True)),
            ('playing_time', models.TimeField(_("Playing time"), null=True, blank=True)),
            ('isbn10', models.CharField(_("ISBN-10"), max_length=13, blank=True)),
            ('isbn13', models.CharField(_("ISBN-13"), max_length=17, blank=True)),
            ('pages', models.PositiveIntegerField(_("Pages"), default=0, null=True, blank=True)),
            ('file_size', models.PositiveIntegerField(_("File size (MB)"), default=0, null=True, blank=True)),
            ('image', FileBrowseField(_('Image'), extensions=['.jpg','.jpeg','.gif','.png','.tif','.tiff'], max_length=255, directory="/%s/"%URL_ID_DOCUMENTS, blank=True)),
            ('status', models.ForeignKey(orm['structure.Term'], limit_choices_to={'vocabulary__sysname':'basics_object_statuses'}, related_name="status_documents", default=DefaultObjectStatus("draft"), blank=True, null=True)),
        ))
        db.send_create_signal('resources', ['Document'])
        
        # Adding ManyToManyField 'Document.authors'
        db.create_table('resources_document_authors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('document', models.ForeignKey(orm.Document, null=False)),
            ('person', models.ForeignKey(orm['people.Person'], null=False))
        ))
        
        # Adding ManyToManyField 'Document.languages'
        db.create_table('resources_document_languages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('document', models.ForeignKey(orm.Document, null=False)),
            ('language', models.ForeignKey(orm['i18n.Language'], null=False))
        ))
        
        # Adding ManyToManyField 'Document.creative_sectors'
        db.create_table('resources_document_creative_sectors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('document', models.ForeignKey(orm.Document, null=False)),
            ('term', models.ForeignKey(orm['structure.Term'], null=False))
        ))
        
        # Adding ManyToManyField 'Document.context_categories'
        db.create_table('resources_document_context_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('document', models.ForeignKey(orm.Document, null=False)),
            ('contextcategory', models.ForeignKey(orm['structure.ContextCategory'], null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Document'
        db.delete_table('resources_document')
        
        # Dropping ManyToManyField 'Document.authors'
        db.delete_table('resources_document_authors')
        
        # Dropping ManyToManyField 'Document.languages'
        db.delete_table('resources_document_languages')
        
        # Dropping ManyToManyField 'Document.creative_sectors'
        db.delete_table('resources_document_creative_sectors')
        
        # Dropping ManyToManyField 'Document.context_categories'
        db.delete_table('resources_document_context_categories')
        
    
    
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
            'description': ('models.TextField', ['_("Description (English)")'], {'blank': 'True'}),
            'description_de': ('models.TextField', ['_("Description (German)")'], {'blank': 'True'}),
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
            'title': ('models.CharField', ['_("Title (English)")'], {'max_length': '255'}),
            'title_de': ('models.CharField', ['_("Title (German)")'], {'max_length': '255', 'blank': 'True'}),
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
