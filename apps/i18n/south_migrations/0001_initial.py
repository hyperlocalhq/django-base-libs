# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from jetson.apps.i18n.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Area'
        db.create_table('i18n_area', south_cleaned_fields((
            ('country', models.ForeignKey(orm.Country)),
            ('name_id', models.CharField(_('name identifier'), max_length=6, primary_key=True)),
            ('name', models.CharField(_('area name'), max_length=50)),
            ('alt_name', models.CharField(_('area alternate name'), max_length=50, blank=True)),
            ('abbrev', models.CharField(_('postal abbreviation'), max_length=3, blank=True)),
            ('reg_area', models.CharField(_('regional administrative area'), blank=True, max_length=1)),
        )))
        db.send_create_signal('i18n', ['Area'])
        
        # Adding model 'Phone'
        db.create_table('i18n_phone', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('country', models.ForeignKey(orm.Country)),
            ('code', models.PositiveSmallIntegerField(_('country code'), null=True, blank=True)),
            ('ln_area', models.CharField(_('length of area code'), max_length=10, blank=True)),
            ('ln_sn', models.CharField(_('length of subscriber number (SN)'), max_length=8, blank=True)),
            ('ln_area_sn', models.CharField(_('length of area code and SN'), max_length=8, blank=True)),
            ('nat_prefix', models.CharField(_('national prefix'), max_length=2, blank=True)),
            ('int_prefix', models.CharField(_('international prefix'), max_length=4, blank=True)),
        )))
        db.send_create_signal('i18n', ['Phone'])
        
        # Adding model 'CountryLanguage'
        db.create_table('i18n_countrylanguage', south_cleaned_fields((
            ('country', models.ForeignKey(orm.Country)),
            ('language', models.ForeignKey(orm.Language)),
            ('lang_type', models.CharField(_('language type'), blank=True, max_length=1)),
            ('identifier', models.CharField(_('identifier'), max_length=6, primary_key=True)),
        )))
        db.send_create_signal('i18n', ['CountryLanguage'])
        
        # Adding model 'Country'
        db.create_table('i18n_country', south_cleaned_fields((
            ('name', models.CharField(_('Country Name (English)'), unique=True, max_length=56)),
            ('name_de', models.CharField(_('Country Name (German)'), max_length=56, blank=True)),
            ('iso3_code', models.CharField(_('Alpha-3 ISO Code'), max_length=3)),
            ('iso2_code', models.CharField(_('Alpha-2 ISO Code'), unique=True, max_length=2, primary_key=True)),
            ('region', models.CharField(_('Geographical Region'), max_length=5)),
            ('territory_of', models.CharField(_('Territory of'), max_length=3, blank=True)),
            ('adm_area', models.CharField(_('Administrative Area'), blank=True, max_length=2)),
            ('display', models.BooleanField(_('Display'), default=True)),
            ('sort_order', models.PositiveIntegerField(_('Sort Order'), default=20)),
        )))
        db.send_create_signal('i18n', ['Country'])
        
        # Adding model 'Language'
        db.create_table('i18n_language', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('iso3_code', models.CharField(_('Alpha-3 ISO Code'), max_length=3)),
            ('name', models.CharField(_('Language Name (English)'), unique=True, max_length=40)),
            ('name_de', models.CharField(_('Language Name (German)'), max_length=40, blank=True)),
            ('iso2_code', models.CharField(_('Alpha-2 ISO Code'), max_length=2, blank=True)),
            ('synonym', models.CharField(_('Language Synonym'), max_length=40, blank=True)),
            ('display', models.BooleanField(_('Display'), default=False)),
            ('sort_order', models.PositiveIntegerField(_('Sort order'), default=20)),
        )))
        db.send_create_signal('i18n', ['Language'])
        
        # Adding model 'TimeZone'
        db.create_table('i18n_timezone', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('country', models.ForeignKey(orm.Country)),
            ('zone', models.CharField(_('time zone'), unique=True, max_length=32)),
        )))
        db.send_create_signal('i18n', ['TimeZone'])
        
        # Adding model 'Nationality'
        db.create_table('i18n_nationality', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(_('Nationality Name (English)'), unique=True, max_length=40)),
            ('name_de', models.CharField(_('Nationality Name (German)'), max_length=40, blank=True)),
            ('display', models.BooleanField(_('Display'), default=False)),
            ('sort_order', models.PositiveIntegerField(_('Sort order'), default=20)),
        )))
        db.send_create_signal('i18n', ['Nationality'])
        
        # Creating unique_together for [country, name] on Area.
        db.create_unique('i18n_area', ['country_id', 'name'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Area'
        db.delete_table('i18n_area')
        
        # Deleting model 'Phone'
        db.delete_table('i18n_phone')
        
        # Deleting model 'CountryLanguage'
        db.delete_table('i18n_countrylanguage')
        
        # Deleting model 'Country'
        db.delete_table('i18n_country')
        
        # Deleting model 'Language'
        db.delete_table('i18n_language')
        
        # Deleting model 'TimeZone'
        db.delete_table('i18n_timezone')
        
        # Deleting model 'Nationality'
        db.delete_table('i18n_nationality')
        
        # Deleting unique_together for [country, name] on Area.
        db.delete_unique('i18n_area', ['country_id', 'name'])
        
    
    
    models = {
        'i18n.area': {
            'Meta': {'ordering': "['country']", 'unique_together': "(('country','name'),)"},
            'abbrev': ('models.CharField', ["_('postal abbreviation')"], {'max_length': '3', 'blank': 'True'}),
            'alt_name': ('models.CharField', ["_('area alternate name')"], {'max_length': '50', 'blank': 'True'}),
            'country': ('models.ForeignKey', ["orm['i18n.Country']"], {}),
            'name': ('models.CharField', ["_('area name')"], {'max_length': '50'}),
            'name_id': ('models.CharField', ["_('name identifier')"], {'max_length': '6', 'primary_key': 'True'}),
            'reg_area': ('models.CharField', ["_('regional administrative area')"], {'blank': 'True', 'max_length': '1'})
        },
        'i18n.phone': {
            'Meta': {'ordering': "['country']"},
            'code': ('models.PositiveSmallIntegerField', ["_('country code')"], {'null': 'True', 'blank': 'True'}),
            'country': ('models.ForeignKey', ["orm['i18n.Country']"], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'int_prefix': ('models.CharField', ["_('international prefix')"], {'max_length': '4', 'blank': 'True'}),
            'ln_area': ('models.CharField', ["_('length of area code')"], {'max_length': '10', 'blank': 'True'}),
            'ln_area_sn': ('models.CharField', ["_('length of area code and SN')"], {'max_length': '8', 'blank': 'True'}),
            'ln_sn': ('models.CharField', ["_('length of subscriber number (SN)')"], {'max_length': '8', 'blank': 'True'}),
            'nat_prefix': ('models.CharField', ["_('national prefix')"], {'max_length': '2', 'blank': 'True'})
        },
        'i18n.countrylanguage': {
            'Meta': {'ordering': "['country']"},
            'country': ('models.ForeignKey', ["orm['i18n.Country']"], {}),
            'identifier': ('models.CharField', ["_('identifier')"], {'max_length': '6', 'primary_key': 'True'}),
            'lang_type': ('models.CharField', ["_('language type')"], {'blank': 'True', 'max_length': '1'}),
            'language': ('models.ForeignKey', ["orm['i18n.Language']"], {})
        },
        'i18n.country': {
            'Meta': {'ordering': "['sort_order','name']"},
            'adm_area': ('models.CharField', ["_('Administrative Area')"], {'blank': 'True', 'max_length': '2'}),
            'display': ('models.BooleanField', ["_('Display')"], {'default': 'True'}),
            'iso2_code': ('models.CharField', ["_('Alpha-2 ISO Code')"], {'unique': 'True', 'max_length': '2', 'primary_key': 'True'}),
            'iso3_code': ('models.CharField', ["_('Alpha-3 ISO Code')"], {'max_length': '3'}),
            'name': ('models.CharField', ["_('Country Name (English)')"], {'unique': 'True', 'max_length': '56'}),
            'name_de': ('models.CharField', ["_('Country Name (German)')"], {'max_length': '56', 'blank': 'True'}),
            'region': ('models.CharField', ["_('Geographical Region')"], {'max_length': '5'}),
            'sort_order': ('models.PositiveIntegerField', ["_('Sort Order')"], {'default': '20'}),
            'territory_of': ('models.CharField', ["_('Territory of')"], {'max_length': '3', 'blank': 'True'})
        },
        'i18n.language': {
            'Meta': {'ordering': "['sort_order','name']"},
            'display': ('models.BooleanField', ["_('Display')"], {'default': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'iso2_code': ('models.CharField', ["_('Alpha-2 ISO Code')"], {'max_length': '2', 'blank': 'True'}),
            'iso3_code': ('models.CharField', ["_('Alpha-3 ISO Code')"], {'max_length': '3'}),
            'name': ('models.CharField', ["_('Language Name (English)')"], {'unique': 'True', 'max_length': '40'}),
            'name_de': ('models.CharField', ["_('Language Name (German)')"], {'max_length': '40', 'blank': 'True'}),
            'sort_order': ('models.PositiveIntegerField', ["_('Sort order')"], {'default': '20'}),
            'synonym': ('models.CharField', ["_('Language Synonym')"], {'max_length': '40', 'blank': 'True'})
        },
        'i18n.timezone': {
            'Meta': {'ordering': "['zone']"},
            'country': ('models.ForeignKey', ["orm['i18n.Country']"], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'zone': ('models.CharField', ["_('time zone')"], {'unique': 'True', 'max_length': '32'})
        },
        'i18n.nationality': {
            'Meta': {'ordering': "['sort_order','name']"},
            'display': ('models.BooleanField', ["_('Display')"], {'default': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', ["_('Nationality Name (English)')"], {'unique': 'True', 'max_length': '40'}),
            'name_de': ('models.CharField', ["_('Nationality Name (German)')"], {'max_length': '40', 'blank': 'True'}),
            'sort_order': ('models.PositiveIntegerField', ["_('Sort order')"], {'default': '20'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['i18n']
