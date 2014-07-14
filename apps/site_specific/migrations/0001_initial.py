# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from ccb.apps.site_specific.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'ClaimRequest'
        db.create_table('system_claimrequest', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('content_type', models.ForeignKey(orm['contenttypes.ContentType'], related_name=None, null=False, blank=False)),
            ('object_id', models.CharField(u'Related object', max_length=255, null=False, blank=False)),
            ('user', models.ForeignKey(orm['auth.User'], related_name="claimrequest_user")),
            ('name', models.CharField(_('Name'), max_length=80)),
            ('email', models.EmailField(_('Email'))),
            ('phone_country', models.CharField(_("Country Code"), max_length=4, null=True, blank=True)),
            ('phone_area', models.CharField(_("Area Code"), max_length=5, null=True, blank=True)),
            ('phone_number', models.CharField(_("Phone Number"), max_length=15, null=True, blank=True)),
            ('best_time_to_call', models.CharField(_("Best Time to Call"), blank=True, max_length=25, null=True)),
            ('role', models.CharField(_('Role'), max_length=80, null=True, blank=True)),
            ('comments', models.TextField(_('Comments'), null=True, blank=True)),
            ('created_date', models.DateTimeField(_("Created"), auto_now_add=True)),
            ('modified_date', models.DateTimeField(_("Modified"), auto_now=True)),
            ('modifier', models.ForeignKey(orm['auth.User'], related_name="claimrequest_modifier", null=True, blank=True)),
            ('status', models.IntegerField(_("Status"), blank=True, null=True)),
        )))
        db.send_create_signal('site_specific', ['ClaimRequest'])
        
        # Adding model 'ContextItem'
        db.create_table('system_contextitem', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('creation_date', models.DateTimeField(_("creation date"), editable=False)),
            ('modified_date', models.DateTimeField(_("modified date"), null=True, editable=False)),
            ('content_type', models.ForeignKey(orm['contenttypes.ContentType'], related_name=None, null=False, blank=False)),
            ('object_id', models.CharField(u'Related object', max_length=255, null=False, blank=False)),
            ('slug', models.SlugField(unique=True, max_length=255)),
            ('title', models.CharField(_("Title (English)"), max_length=255, blank=True)),
            ('title_de', models.CharField(_("Title (German)"), max_length=255, blank=True)),
            ('description', models.TextField(_("Description (English)"), blank=True)),
            ('description_de', models.TextField(_("Description (German)"), blank=True)),
            ('location_type', models.ForeignKey(orm['structure.Term'], limit_choices_to={'vocabulary__sysname':'basics_locality'}, related_name="locality_contextitems", null=True, blank=True)),
            ('status', models.ForeignKey(orm['structure.Term'], limit_choices_to={'vocabulary__sysname':'basics_object_statuses'}, related_name="status_contextitems", null=True, blank=True)),
            ('additional_search_data', models.TextField(null=True, blank=True)),
        )))
        db.send_create_signal('site_specific', ['ContextItem'])
        
        # Adding ManyToManyField 'ContextItem.creative_sectors'
        db.create_table('system_contextitem_creative_sectors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('contextitem', models.ForeignKey(orm.ContextItem, null=False)),
            ('term', models.ForeignKey(orm['structure.Term'], null=False))
        ))
        
        # Adding ManyToManyField 'ContextItem.object_types'
        db.create_table('system_contextitem_object_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('contextitem', models.ForeignKey(orm.ContextItem, null=False)),
            ('term', models.ForeignKey(orm['structure.Term'], null=False))
        ))
        
        # Adding ManyToManyField 'ContextItem.context_categories'
        db.create_table('system_contextitem_context_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('contextitem', models.ForeignKey(orm.ContextItem, null=False)),
            ('contextcategory', models.ForeignKey(orm['structure.ContextCategory'], null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'ClaimRequest'
        db.delete_table('system_claimrequest')
        
        # Deleting model 'ContextItem'
        db.delete_table('system_contextitem')
        
        # Dropping ManyToManyField 'ContextItem.creative_sectors'
        db.delete_table('system_contextitem_creative_sectors')
        
        # Dropping ManyToManyField 'ContextItem.object_types'
        db.delete_table('system_contextitem_object_types')
        
        # Dropping ManyToManyField 'ContextItem.context_categories'
        db.delete_table('system_contextitem_context_categories')
        
    
    
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
            'description': ('models.TextField', ['_("Description (English)")'], {'blank': 'True'}),
            'description_de': ('models.TextField', ['_("Description (German)")'], {'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'location_type': ('models.ForeignKey', ["orm['structure.Term']"], {'limit_choices_to': "{'vocabulary__sysname':'basics_locality'}", 'related_name': '"locality_contextitems"', 'null': 'True', 'blank': 'True'}),
            'modified_date': ('models.DateTimeField', ['_("modified date")'], {'null': 'True', 'editable': 'False'}),
            'object_id': ('models.CharField', ["u'Related object'"], {'max_length': '255', 'null': 'False', 'blank': 'False'}),
            'object_types': ('models.ManyToManyField', ["orm['structure.Term']"], {'limit_choices_to': "{'vocabulary__sysname':'basics_object_types'}", 'related_name': '"object_type_contextitems"', 'blank': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'status': ('models.ForeignKey', ["orm['structure.Term']"], {'limit_choices_to': "{'vocabulary__sysname':'basics_object_statuses'}", 'related_name': '"status_contextitems"', 'null': 'True', 'blank': 'True'}),
            'title': ('models.CharField', ['_("Title (English)")'], {'max_length': '255', 'blank': 'True'}),
            'title_de': ('models.CharField', ['_("Title (German)")'], {'max_length': '255', 'blank': 'True'})
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
