# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Changing field 'Memo.creation_date'
        db.alter_column(u'memos_memo', 'creation_date', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Memo.content_type'
        db.alter_column(u'memos_memo', 'content_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True))

        # Changing field 'Memo.collection'
        db.alter_column(u'memos_memo', 'collection_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['memos.MemoCollection']))

        # Changing field 'Memo.object_id'
        db.alter_column(u'memos_memo', 'object_id', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'MemoCollection.token'
        db.alter_column(u'memos_memocollection', 'token', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20))

        # Changing field 'MemoCollection.creation_date'
        db.alter_column(u'memos_memocollection', 'creation_date', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'MemoCollection.expiration'
        db.alter_column(u'memos_memocollection', 'expiration', self.gf('django.db.models.fields.DateTimeField')())
    
    
    def backwards(self, orm):
        
        # Changing field 'Memo.creation_date'
        db.alter_column(u'memos_memo', 'creation_date', self.gf('models.DateTimeField')(_("creation date"), editable=False))

        # Changing field 'Memo.content_type'
        db.alter_column(u'memos_memo', 'content_type_id', self.gf('models.ForeignKey')(orm['contenttypes.ContentType'], limit_choices_to={}, null=True))

        # Changing field 'Memo.collection'
        db.alter_column(u'memos_memo', 'collection_id', self.gf('models.ForeignKey')(orm['memos.MemoCollection']))

        # Changing field 'Memo.object_id'
        db.alter_column(u'memos_memo', 'object_id', self.gf('models.CharField')(u'Related object', max_length=255, null=False))

        # Changing field 'MemoCollection.token'
        db.alter_column(u'memos_memocollection', 'token', self.gf('models.CharField')(_("Token"), max_length=20, unique=True))

        # Changing field 'MemoCollection.creation_date'
        db.alter_column(u'memos_memocollection', 'creation_date', self.gf('models.DateTimeField')(_("creation date"), editable=False))

        # Changing field 'MemoCollection.expiration'
        db.alter_column(u'memos_memocollection', 'expiration', self.gf('models.DateTimeField')(_("Expiration")))
    
    
    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('app_label', 'name')", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'memos.memo': {
            'Meta': {'object_name': 'Memo'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['memos.MemoCollection']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        u'memos.memocollection': {
            'Meta': {'object_name': 'MemoCollection'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'expiration': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['memos']
