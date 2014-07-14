# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from ccb.apps.site_specific.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'ContextItem.title_en'
        db.add_column('system_contextitem', 'title_en', models.CharField(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False))
        
        # Adding field 'ContextItem.description_de_markup_type'
        db.add_column('system_contextitem', 'description_de_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False))
        
        # Adding field 'ContextItem.description_en'
        db.add_column('system_contextitem', 'description_en', ExtendedTextField(u'Description', unique_for_month=None, unique=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, null=False, unique_for_date=None, db_tablespace='', db_index=False))
        
        # Adding field 'ContextItem.description_en_markup_type'
        db.add_column('system_contextitem', 'description_en_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False))
        
        # Adding field 'ContextItem.description_markup_type'
        db.add_column('system_contextitem', 'description_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False))
        
        # Changing field 'ContextItem.title_de'
        db.alter_column('system_contextitem', 'title_de', models.CharField(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False))
        
        # Changing field 'ContextItem.description'
        db.alter_column('system_contextitem', 'description', MultilingualTextField(_("Description"), blank=True))
        
        # Changing field 'ContextItem.title'
        db.alter_column('system_contextitem', 'title', MultilingualCharField(_("Title"), max_length=255, blank=True))
        
        # Changing field 'ContextItem.description_de'
        db.alter_column('system_contextitem', 'description_de', ExtendedTextField(u'Description', unique_for_month=None, unique=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, null=False, unique_for_date=None, db_tablespace='', db_index=False))
        
    
    def backwards(self, orm):
        
        # Deleting field 'ContextItem.title_en'
        db.delete_column('system_contextitem', 'title_en')
        
        # Deleting field 'ContextItem.description_de_markup_type'
        db.delete_column('system_contextitem', 'description_de_markup_type')
        
        # Deleting field 'ContextItem.description_en'
        db.delete_column('system_contextitem', 'description_en')
        
        # Deleting field 'ContextItem.description_en_markup_type'
        db.delete_column('system_contextitem', 'description_en_markup_type')
        
        # Deleting field 'ContextItem.description_markup_type'
        db.delete_column('system_contextitem', 'description_markup_type')
        
        # Changing field 'ContextItem.title_de'
        db.alter_column('system_contextitem', 'title_de', models.CharField(_("Title (German)"), max_length=255, blank=True))
        
        # Changing field 'ContextItem.description'
        db.alter_column('system_contextitem', 'description', models.TextField(_("Description (English)"), blank=True))
        
        # Changing field 'ContextItem.title'
        db.alter_column('system_contextitem', 'title', models.CharField(_("Title (English)"), max_length=255, blank=True))
        
        # Changing field 'ContextItem.description_de'
        db.alter_column('system_contextitem', 'description_de', models.TextField(_("Description (German)"), blank=True))
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'structure.contextcategory': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'site_specific.contextitem': {
            'Meta': {'ordering': "XFieldList(['title_','creation_date'])", 'db_table': '"system_contextitem"'},
            'additional_search_data': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'related_name': 'None', 'null': 'False', 'blank': 'False'}),
            'context_categories': ('models.ManyToManyField', ["orm['structure.ContextCategory']"], {'blank': 'True'}),
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'editable': 'False'}),
            'creative_sectors': ('models.ManyToManyField', ["orm['structure.Term']"], {'limit_choices_to': "{'vocabulary__sysname':'categories_creativesectors'}", 'related_name': '"creative_industry_contextitems"', 'blank': 'True'}),
            'description': ('MultilingualTextField', ['_("Description")'], {'blank': 'True'}),
            'description_de': ('ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'location_type': ('models.ForeignKey', ["orm['structure.Term']"], {'limit_choices_to': "{'vocabulary__sysname':'basics_locality'}", 'related_name': '"locality_contextitems"', 'null': 'True', 'blank': 'True'}),
            'modified_date': ('models.DateTimeField', ['_("modified date")'], {'null': 'True', 'editable': 'False'}),
            'object_id': ('models.CharField', ["u'Related object'"], {'max_length': '255', 'null': 'False', 'blank': 'False'}),
            'object_types': ('models.ManyToManyField', ["orm['structure.Term']"], {'limit_choices_to': "{'vocabulary__sysname':'basics_object_types'}", 'related_name': '"object_type_contextitems"', 'blank': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'status': ('models.ForeignKey', ["orm['structure.Term']"], {'limit_choices_to': "{'vocabulary__sysname':'basics_object_statuses'}", 'related_name': '"status_contextitems"', 'null': 'True', 'blank': 'True'}),
            'title': ('MultilingualCharField', ['_("Title")'], {'max_length': '255', 'blank': 'True'}),
            'title_de': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'structure.term': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'site_specific.claimrequest': {
            'Meta': {'ordering': "('-created_date',)", 'db_table': '"system_claimrequest"'},
            'best_time_to_call': ('models.CharField', ['_("Best Time to Call")'], {'blank': 'True', 'max_length': '25', 'null': 'True'}),
            'comments': ('models.TextField', ["_('Comments')"], {'null': 'True', 'blank': 'True'}),
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'related_name': 'None', 'null': 'False', 'blank': 'False'}),
            'created_date': ('models.DateTimeField', ['_("Created")'], {'auto_now_add': 'True'}),
            'email': ('models.EmailField', ["_('Email')"], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('models.DateTimeField', ['_("Modified")'], {'auto_now': 'True'}),
            'modifier': ('models.ForeignKey', ["orm['auth.User']"], {'related_name': '"claimrequest_modifier"', 'null': 'True', 'blank': 'True'}),
            'name': ('models.CharField', ["_('Name')"], {'max_length': '80'}),
            'object_id': ('models.CharField', ["u'Related object'"], {'max_length': '255', 'null': 'False', 'blank': 'False'}),
            'phone_area': ('models.CharField', ['_("Area Code")'], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'phone_country': ('models.CharField', ['_("Country Code")'], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'phone_number': ('models.CharField', ['_("Phone Number")'], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'role': ('models.CharField', ["_('Role')"], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'status': ('models.IntegerField', ['_("Status")'], {'blank': 'True', 'null': 'True'}),
            'user': ('models.ForeignKey', ["orm['auth.User']"], {'related_name': '"claimrequest_user"'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['site_specific']
