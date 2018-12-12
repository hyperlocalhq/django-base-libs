# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from jetson.apps.permissions.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'RowLevelPermission'
        db.create_table('auth_rowlevelpermission', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('owner_content_type', models.ForeignKey(orm['contenttypes.ContentType'], related_name='owner', null=False, blank=False)),
            ('owner_object_id', models.CharField(u'Owner', max_length=255, null=False, blank=False)),
            ('content_type', models.ForeignKey(orm['contenttypes.ContentType'], related_name=None, null=False, blank=False)),
            ('object_id', models.CharField(u'Related object', max_length=255, null=False, blank=False)),
            ('negative', models.BooleanField()),
            ('permission', models.ForeignKey(orm['auth.Permission'])),
        )))
        db.send_create_signal('permissions', ['RowLevelPermission'])
        
        # Adding model 'PerObjectGroup'
        db.create_table('auth_perobjectgroup', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('content_type', models.ForeignKey(orm['contenttypes.ContentType'], related_name=None, null=False, blank=False)),
            ('object_id', models.CharField(u'Related object', max_length=255, null=False, blank=False)),
            ('sysname', models.SlugField(unique=True, max_length=80)),
            ('title', MultilingualCharField(_('title'), max_length=80)),
            ('title_de', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=80, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('title_en', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=80, db_tablespace='', blank=False, unique=False, db_index=False)),
        )))
        db.send_create_signal('permissions', ['PerObjectGroup'])
        
        # Adding ManyToManyField 'PerObjectGroup.users'
        db.create_table('auth_perobjectgroup_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('perobjectgroup', models.ForeignKey(orm.PerObjectGroup, null=False)),
            ('user', models.ForeignKey(orm['auth.User'], null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'RowLevelPermission'
        db.delete_table('auth_rowlevelpermission')
        
        # Deleting model 'PerObjectGroup'
        db.delete_table('auth_perobjectgroup')
        
        # Dropping ManyToManyField 'PerObjectGroup.users'
        db.delete_table('auth_perobjectgroup_users')
        
    
    
    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label','codename')", 'unique_together': "(('content_type','codename'),)"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'permissions.rowlevelpermission': {
            'Meta': {'db_table': '"auth_rowlevelpermission"'},
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'related_name': 'None', 'null': 'False', 'blank': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'negative': ('models.BooleanField', [], {}),
            'object_id': ('models.CharField', ["u'Related object'"], {'max_length': '255', 'null': 'False', 'blank': 'False'}),
            'owner_content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'related_name': "'owner'", 'null': 'False', 'blank': 'False'}),
            'owner_object_id': ('models.CharField', ["u'Owner'"], {'max_length': '255', 'null': 'False', 'blank': 'False'}),
            'permission': ('models.ForeignKey', ["orm['auth.Permission']"], {})
        },
        'permissions.perobjectgroup': {
            'Meta': {'ordering': "('sysname',)", 'db_table': '"auth_perobjectgroup"'},
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'related_name': 'None', 'null': 'False', 'blank': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('models.CharField', ["u'Related object'"], {'max_length': '255', 'null': 'False', 'blank': 'False'}),
            'sysname': ('models.SlugField', [], {'unique': 'True', 'max_length': '80'}),
            'title': ('MultilingualCharField', ["_('title')"], {'max_length': '80'}),
            'title_de': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '80', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '80', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'users': ('models.ManyToManyField', ["orm['auth.User']"], {'blank': 'True'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['permissions']
