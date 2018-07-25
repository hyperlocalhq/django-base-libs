# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from jetson.apps.profanity_filter.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'SwearingCase.modified_date'
        db.add_column('profanity_filter_swearingcase', 'modified_date', orm['profanity_filter.swearingcase:modified_date'])
        
        # Changing field 'SwearingCase.creation_date'
        # (to signature: django.db.models.fields.DateTimeField())
        db.alter_column('profanity_filter_swearingcase', 'creation_date', orm['profanity_filter.swearingcase:creation_date'])
        
        # Changing field 'SwearingCase.used_words'
        # (to signature: django.db.models.fields.TextField())
        db.alter_column('profanity_filter_swearingcase', 'used_words', orm['profanity_filter.swearingcase:used_words'])
        
        # Changing field 'SwearingCase.user'
        # (to signature: django.db.models.fields.related.ForeignKey(to=orm['auth.User'], null=True, blank=True))
        db.alter_column('profanity_filter_swearingcase', 'user_id', orm['profanity_filter.swearingcase:user'])
        
        # Changing field 'SwearWord.word'
        # (to signature: django.db.models.fields.CharField(max_length=80))
        db.alter_column('profanity_filter_swearword', 'word', orm['profanity_filter.swearword:word'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'SwearingCase.modified_date'
        db.delete_column('profanity_filter_swearingcase', 'modified_date')
        
        # Changing field 'SwearingCase.creation_date'
        # (to signature: models.DateTimeField(_("creation date"), editable=False))
        db.alter_column('profanity_filter_swearingcase', 'creation_date', orm['profanity_filter.swearingcase:creation_date'])
        
        # Changing field 'SwearingCase.used_words'
        # (to signature: models.TextField(_("used words")))
        db.alter_column('profanity_filter_swearingcase', 'used_words', orm['profanity_filter.swearingcase:used_words'])
        
        # Changing field 'SwearingCase.user'
        # (to signature: models.ForeignKey(orm['auth.User'], null=True, blank=True))
        db.alter_column('profanity_filter_swearingcase', 'user_id', orm['profanity_filter.swearingcase:user'])
        
        # Changing field 'SwearWord.word'
        # (to signature: models.CharField(_("Word to filter out"), max_length=80))
        db.alter_column('profanity_filter_swearword', 'word', orm['profanity_filter.swearword:word'])
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'row_level_permissions_owned': ('django.contrib.contenttypes.generic.GenericRelation', [], {'object_id_field': "'owner_object_id'", 'content_type_field': "'owner_content_type'", 'to': "orm['permissions.RowLevelPermission']"}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'permissions.rowlevelpermission': {
            'Meta': {'db_table': "'auth_rowlevelpermission'"},
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'related_name': 'None', 'null': 'False', 'blank': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'negative': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'object_id': ('models.CharField', ["u'Related object'"], {'max_length': '255', 'null': 'False', 'blank': 'False'}),
            'owner_content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'related_name': "'owner'", 'null': 'False', 'blank': 'False'}),
            'owner_object_id': ('models.CharField', ["u'Owner'"], {'max_length': '255', 'null': 'False', 'blank': 'False'}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.Permission']"})
        },
        'profanity_filter.swearingcase': {
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'related_name': 'None', 'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'object_id': ('models.CharField', ["u'Related object'"], {'max_length': '255', 'null': 'False', 'blank': 'True'}),
            'used_words': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'profanity_filter.swearword': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'word': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['profanity_filter']
