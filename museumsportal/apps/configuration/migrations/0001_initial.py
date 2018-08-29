# -*- coding: UTF-8 -*-
from south.db import db
from django.db import models
from museumsportal.apps.configuration.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'PageSettings'
        db.create_table('configuration_pagesettings', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('site', models.ForeignKey(orm['sites.Site'], unique=True)),
            ('user', models.ForeignKey(orm['auth.User'], null=True)),
            ('path', models.CharField(_('Path'), max_length=100, blank=True)),
            ('pickled_settings', models.TextField(_('Settings'), editable=False)),
        )))
        db.send_create_signal('configuration', ['PageSettings'])
        
        # Adding model 'SiteSettings'
        db.create_table('configuration_sitesettings', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('meta_keywords', MultilingualCharField(_('Keywords'), max_length=255, blank=True)),
            ('meta_description', MultilingualCharField(_('Description'), max_length=255, blank=True)),
            ('meta_author', models.CharField(_('Author'), max_length=255, blank=True)),
            ('meta_copyright', models.CharField(_('Copyright'), max_length=255, blank=True)),
            ('site', models.ForeignKey(orm['sites.Site'], unique=True)),
            ('registration_type', models.CharField(_("Registration type"), default='simple', max_length=10)),
            ('login_by_email', models.BooleanField(_("Login by email"))),
            ('gmaps_api_key', models.CharField(_("Google Maps API Key"), default='ABQIAAAACeM7_PeKjcwohDMmjxqD1RT1e54QDoeePfsGQUixHoyyb7eTxhTO-Ji1lhmrD0-TMcZt7uteQOa-GQ', max_length=200, blank=True)),
            ('extra_head', PlainTextModelField(_("Extra head"), blank=True)),
            ('extra_body', PlainTextModelField(_("Extra body"), blank=True)),
            ('meta_keywords_de', models.CharField(u'Keywords', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('meta_keywords_en', models.CharField(u'Keywords', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('meta_description_de', models.CharField(u'Description', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('meta_description_en', models.CharField(u'Description', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
        )))
        db.send_create_signal('configuration', ['SiteSettings'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'PageSettings'
        db.delete_table('configuration_pagesettings')
        
        # Deleting model 'SiteSettings'
        db.delete_table('configuration_sitesettings')
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'configuration.pagesettings': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'path': ('models.CharField', ["_('Path')"], {'max_length': '100', 'blank': 'True'}),
            'pickled_settings': ('models.TextField', ["_('Settings')"], {'editable': 'False'}),
            'site': ('models.ForeignKey', ["orm['sites.Site']"], {'unique': 'True'}),
            'user': ('models.ForeignKey', ["orm['auth.User']"], {'null': 'True'})
        },
        'configuration.sitesettings': {
            'extra_body': ('PlainTextModelField', ['_("Extra body")'], {'blank': 'True'}),
            'extra_head': ('PlainTextModelField', ['_("Extra head")'], {'blank': 'True'}),
            'gmaps_api_key': ('models.CharField', ['_("Google Maps API Key")'], {'default': "'ABQIAAAACeM7_PeKjcwohDMmjxqD1RT1e54QDoeePfsGQUixHoyyb7eTxhTO-Ji1lhmrD0-TMcZt7uteQOa-GQ'", 'max_length': '200', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'login_by_email': ('models.BooleanField', ['_("Login by email")'], {}),
            'meta_author': ('models.CharField', ["_('Author')"], {'max_length': '255', 'blank': 'True'}),
            'meta_copyright': ('models.CharField', ["_('Copyright')"], {'max_length': '255', 'blank': 'True'}),
            'meta_description': ('MultilingualCharField', ["_('Description')"], {'max_length': '255', 'blank': 'True'}),
            'meta_description_de': ('models.CharField', ["u'Description'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'meta_description_en': ('models.CharField', ["u'Description'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'meta_keywords': ('MultilingualCharField', ["_('Keywords')"], {'max_length': '255', 'blank': 'True'}),
            'meta_keywords_de': ('models.CharField', ["u'Keywords'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'meta_keywords_en': ('models.CharField', ["u'Keywords'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'registration_type': ('models.CharField', ['_("Registration type")'], {'default': "'simple'", 'max_length': '10'}),
            'site': ('models.ForeignKey', ["orm['sites.Site']"], {'unique': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'db_table': "'django_site'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['configuration']
