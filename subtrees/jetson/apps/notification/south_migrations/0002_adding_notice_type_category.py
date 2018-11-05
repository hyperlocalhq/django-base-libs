# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from jetson.apps.notification.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        # Adding model 'NoticeSettingCategory'
        db.create_table('notification_noticetypecategory', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('title', MultilingualCharField(_('title'), max_length=50)),
            ('is_public', models.BooleanField(_('is this notice type displayed in the public notification settings?'), default=True)),
            ('title_en', models.CharField(_('title'), null=False, primary_key=False, db_column=None, default='', editable=True, max_length=50, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('title_de', models.CharField(_('title'), null=False, primary_key=False, db_column=None, default='', editable=True, max_length=50, db_tablespace='', blank=False, unique=False, db_index=False)),
        )))
        db.send_create_signal('notification', ['NoticeTypeCategory'])
    
        # Adding field 'NoticeType.category'
        db.add_column('notification_noticetype', 'category', models.ForeignKey(orm.NoticeTypeCategory, null=True, blank=True))
        
        
    def backwards(self, orm):
        
        # Deleting field 'NoticeType.category'
        db.delete_column('notification_noticetype', 'category_id')
        
        # Deleting model 'NoticeSettingCategory'
        db.delete_table('notification_noticetypecategory')
        
    
    models = {
        'notification.noticesetting': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'medium': ('models.CharField', ["_('medium')"], {'max_length': '1'}),
            'notice_type': ('models.ForeignKey', ["orm['notification.NoticeType']"], {}),
            'send': ('models.BooleanField', ["_('send')"], {}),
            'user': ('models.ForeignKey', ["orm['auth.User']"], {})
        },
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'notification.noticetypecategory': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('models.BooleanField', ["_('is this category displayed in the public notification settings?')"], {'default': 'True'}),
            'title': ('MultilingualCharField', ["_('display')"], {'max_length': '50'}),
            'title_de': ('models.CharField', ["u'display'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '50', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'display'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '50', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'notification.observeditem': {
            'Meta': {'ordering': "['-added']"},
            'added': ('models.DateTimeField', ["_('added')"], {'default': 'datetime.datetime.now'}),
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'related_name': 'None', 'null': 'False', 'blank': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'notice_type': ('models.ForeignKey', ["orm['notification.NoticeType']"], {}),
            'object_id': ('models.CharField', ["u'Related object'"], {'max_length': '255', 'null': 'False', 'blank': 'False'}),
            'signal': ('models.CharField', [], {'max_length': '255'}),
            'user': ('models.ForeignKey', ["orm['auth.User']"], {})
        },
        'notification.noticetype': {
            'category': ('models.ForeignKey', ["orm['notification.NoticeTypeCategory']"], {'null': 'True', 'blank': 'True'}),
            'default': ('models.IntegerField', ["_('default')"], {}),
            'description': ('MultilingualCharField', ["_('description')"], {'max_length': '100'}),
            'description_de': ('models.CharField', ["u'description'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'editable': 'True', 'max_length': '100', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'description_en': ('models.CharField', ["u'description'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'editable': 'True', 'max_length': '100', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'display': ('MultilingualCharField', ["_('display')"], {'max_length': '50'}),
            'display_de': ('models.CharField', ["u'display'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '50', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'display_en': ('models.CharField', ["u'display'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '50', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('models.BooleanField', ["_('is this notice type displayed in the public notification settings?')"], {'default': 'True'}),
            'message_template': ('MultilingualPlainTextField', ['_("Message Template")'], {}),
            'message_template_de': ('PlainTextModelField', ["u'Message Template'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'False', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'message_template_en': ('PlainTextModelField', ["u'Message Template'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'False', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'sysname': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'})
        },
        'notification.notice': {
            'Meta': {'ordering': '["-added"]'},
            'added': ('models.DateTimeField', ["_('added')"], {'default': 'datetime.datetime.now'}),
            'archived': ('models.BooleanField', ["_('archived')"], {'default': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'message': ('models.TextField', ["_('message')"], {}),
            'notice_type': ('models.ForeignKey', ["orm['notification.NoticeType']"], {}),
            'unseen': ('models.BooleanField', ["_('unseen')"], {'default': 'True'}),
            'user': ('models.ForeignKey', ["orm['auth.User']"], {})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['notification']
