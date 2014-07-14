# -*- coding: UTF-8 -*-

from django.db import models
from south.db import db

from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

from ccb.apps.external_services.jovoto.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Idea'
        db.create_table('jovoto_idea', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('creation_date', models.DateTimeField(_("creation date"), editable=False)),
            ('modified_date', models.DateTimeField(_("modified date"), null=True, editable=False)),
            ('views', models.IntegerField(_("views"), default=0, editable=False)),
            ('ext_id', models.IntegerField(_("id"))),
            ('name', models.CharField(_("name"), max_length=256)),
            ('description', models.TextField(_("description"))),
            ('pubdate', models.DateTimeField(_("publishing date"))),
            ('link', URLField(_("link"))),
            ('guid', URLField(_("guid"))),
            ('author_username', models.CharField(_("author username"), max_length=256, blank=True)),
            ('author_city', models.CharField(_("author city"), max_length=256, blank=True)),
            ('author_country', models.CharField(_("author country"), max_length=256, blank=True)),
            ('author_icon', models.CharField(_("author icon"), max_length=256, blank=True)),
            ('media0_type', models.CharField(_("first media type"), max_length=256)),
            ('media0_thumb', models.CharField(_("first media thumbnail"), max_length=256, null=True, blank=True)),
            ('media0_medium', models.CharField(_("first media medium sized"), max_length=256, null=True, blank=True)),
            ('media0_big', models.CharField(_("first media big sized"), max_length=256, null=True, blank=True)),
            ('media0_path', models.CharField(_("first media originally sized"), max_length=256, null=True, blank=True)),
            ('rating', models.DecimalField(_("rating"), null=True, max_digits=5, decimal_places=2, blank=True)),
        )))
        db.send_create_signal('jovoto', ['Idea'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Idea'
        db.delete_table('jovoto_idea')
        
    
    
    models = {
        'jovoto.idea': {
            'Meta': {'ordering': "('-pubdate',)"},
            'author_city': ('models.CharField', ['_("author city")'], {'max_length': '256', 'blank': 'True'}),
            'author_country': ('models.CharField', ['_("author country")'], {'max_length': '256', 'blank': 'True'}),
            'author_icon': ('models.CharField', ['_("author icon")'], {'max_length': '256', 'blank': 'True'}),
            'author_username': ('models.CharField', ['_("author username")'], {'max_length': '256', 'blank': 'True'}),
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'editable': 'False'}),
            'description': ('models.TextField', ['_("description")'], {}),
            'ext_id': ('models.IntegerField', ['_("id")'], {}),
            'guid': ('URLField', ['_("guid")'], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'link': ('URLField', ['_("link")'], {}),
            'media0_big': ('models.CharField', ['_("first media big sized")'], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'media0_medium': ('models.CharField', ['_("first media medium sized")'], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'media0_path': ('models.CharField', ['_("first media originally sized")'], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'media0_thumb': ('models.CharField', ['_("first media thumbnail")'], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'media0_type': ('models.CharField', ['_("first media type")'], {'max_length': '256'}),
            'modified_date': ('models.DateTimeField', ['_("modified date")'], {'null': 'True', 'editable': 'False'}),
            'name': ('models.CharField', ['_("name")'], {'max_length': '256'}),
            'pubdate': ('models.DateTimeField', ['_("publishing date")'], {}),
            'rating': ('models.DecimalField', ['_("rating")'], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'views': ('models.IntegerField', ['_("views")'], {'default': '0', 'editable': 'False'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['jovoto']
