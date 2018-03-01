# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from jetson.apps.bookmarks.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Bookmark'
        db.create_table('bookmarks_bookmark', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('creation_date', models.DateTimeField(_("creation date"), editable=False)),
            ('modified_date', models.DateTimeField(_("modified date"), null=True, editable=False)),
            ('creator', models.ForeignKey(orm['auth.User'], editable=False, related_name="%(class)s_creator", null=True)),
            ('title', models.CharField(_("title"), max_length=80)),
            ('url_path', models.CharField(_("URL"), max_length=255)),
        )))
        db.send_create_signal('bookmarks', ['Bookmark'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Bookmark'
        db.delete_table('bookmarks_bookmark')
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'bookmarks.bookmark': {
            'Meta': {'ordering': '["creation_date"]'},
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'editable': 'False'}),
            'creator': ('models.ForeignKey', ["orm['auth.User']"], {'editable': 'False', 'related_name': '"%(class)s_creator"', 'null': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('models.DateTimeField', ['_("modified date")'], {'null': 'True', 'editable': 'False'}),
            'title': ('models.CharField', ['_("title")'], {'max_length': '80'}),
            'url_path': ('models.CharField', ['_("URL")'], {'max_length': '255'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['bookmarks']
