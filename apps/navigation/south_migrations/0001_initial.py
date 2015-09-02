# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from jetson.apps.navigation.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'NavigationLink'
        db.create_table('navigation_navigationlink', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('site', models.ForeignKey(orm['sites.Site'], null=True, blank=True)),
            ('sort_order', models.IntegerField(_("sort order"), editable=False, blank=True)),
            ('parent', models.ForeignKey(orm.NavigationLink, related_name="child_set", null=True, blank=True)),
            ('path', models.CharField(_('path'), editable=False, max_length=8192, null=True)),
            ('content_type', models.ForeignKey(orm['contenttypes.ContentType'], related_name=None, null=True, blank=True)),
            ('object_id', models.CharField(u'Linked object', max_length=255, null=False, blank=True)),
            ('sysname', models.SlugField(unique=True, max_length=255)),
            ('title', MultilingualCharField(_('title'), max_length=255)),
            ('link_url', models.CharField(_("Link URL"), max_length=255, blank=True)),
            ('related_urls', PlainTextModelField(_("Related URLs"), blank=True)),
            ('is_group', models.BooleanField(_("Group of links"), default=False)),
            ('is_group_name_shown', models.BooleanField(_("Show group name"), default=True)),
            ('is_shown_for_visitors', models.BooleanField(_("Shown for visitors"), default=True)),
            ('is_shown_for_users', models.BooleanField(_("Shown for users"), default=True)),
            ('is_login_required', models.BooleanField(_("Require login"), default=False)),
            ('is_promoted', models.BooleanField(_("Promoted"), default=False)),
            ('description', MultilingualTextField(_('description'), blank=True)),
            ('title_de', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('title_en', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('description_de', ExtendedTextField(u'description', unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, unique_for_year=None, rel=None, blank=True, null=False, unique_for_date=None, db_tablespace='', db_index=False)),
            ('description_de_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('description_en', ExtendedTextField(u'description', unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, unique_for_year=None, rel=None, blank=True, null=False, unique_for_date=None, db_tablespace='', db_index=False)),
            ('description_en_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('description_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
        )))
        db.send_create_signal('navigation', ['NavigationLink'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'NavigationLink'
        db.delete_table('navigation_navigationlink')
        
    
    
    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'db_table': "'django_site'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'navigation.navigationlink': {
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'related_name': 'None', 'null': 'True', 'blank': 'True'}),
            'description': ('MultilingualTextField', ["_('description')"], {'blank': 'True'}),
            'description_de': ('ExtendedTextField', ["u'description'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('ExtendedTextField', ["u'description'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'is_group': ('models.BooleanField', ['_("Group of links")'], {'default': 'False'}),
            'is_group_name_shown': ('models.BooleanField', ['_("Show group name")'], {'default': 'True'}),
            'is_login_required': ('models.BooleanField', ['_("Require login")'], {'default': 'False'}),
            'is_promoted': ('models.BooleanField', ['_("Promoted")'], {'default': 'False'}),
            'is_shown_for_users': ('models.BooleanField', ['_("Shown for users")'], {'default': 'True'}),
            'is_shown_for_visitors': ('models.BooleanField', ['_("Shown for visitors")'], {'default': 'True'}),
            'link_url': ('models.CharField', ['_("Link URL")'], {'max_length': '255', 'blank': 'True'}),
            'object_id': ('models.CharField', ["u'Linked object'"], {'max_length': '255', 'null': 'False', 'blank': 'True'}),
            'parent': ('models.ForeignKey', ["orm['navigation.NavigationLink']"], {'related_name': '"child_set"', 'null': 'True', 'blank': 'True'}),
            'path': ('models.CharField', ["_('path')"], {'editable': 'False', 'max_length': '8192', 'null': 'True'}),
            'related_urls': ('PlainTextModelField', ['_("Related URLs")'], {'blank': 'True'}),
            'site': ('models.ForeignKey', ["orm['sites.Site']"], {'null': 'True', 'blank': 'True'}),
            'sort_order': ('models.IntegerField', ['_("sort order")'], {'editable': 'False', 'blank': 'True'}),
            'sysname': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'title': ('MultilingualCharField', ["_('title')"], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['navigation']
