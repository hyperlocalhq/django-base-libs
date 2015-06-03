# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from jetson.apps.memos.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Memo'
        db.create_table('memos_memo', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('creation_date', models.DateTimeField(_("creation date"), editable=False)),
            ('content_type', models.ForeignKey(orm['contenttypes.ContentType'], limit_choices_to={}, related_name=None, null=True, blank=True)),
            ('object_id', models.CharField(u'Related object', max_length=255, null=False, blank=True)),
            ('collection', models.ForeignKey(orm.MemoCollection)),
        )))
        db.send_create_signal('memos', ['Memo'])
        
        # Adding model 'MemoCollection'
        db.create_table('memos_memocollection', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('creation_date', models.DateTimeField(_("creation date"), editable=False)),
            ('token', models.CharField(_("Token"), unique=True, max_length=20)),
            ('expiration', models.DateTimeField(_("Expiration"))),
        )))
        db.send_create_signal('memos', ['MemoCollection'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Memo'
        db.delete_table('memos_memo')
        
        # Deleting model 'MemoCollection'
        db.delete_table('memos_memocollection')
        
    
    
    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'memos.memo': {
            'collection': ('models.ForeignKey', ["orm['memos.MemoCollection']"], {}),
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'limit_choices_to': '{}', 'related_name': 'None', 'null': 'True', 'blank': 'True'}),
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'editable': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('models.CharField', ["u'Related object'"], {'max_length': '255', 'null': 'False', 'blank': 'True'})
        },
        'memos.memocollection': {
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'editable': 'False'}),
            'expiration': ('models.DateTimeField', ['_("Expiration")'], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'token': ('models.CharField', ['_("Token")'], {'unique': 'True', 'max_length': '20'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['memos']
