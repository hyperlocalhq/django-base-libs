# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from jetson.apps.optionset.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'PhoneType'
        db.create_table('optionset_phonetype', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('slug', models.SlugField(unique=True, max_length=255)),
            ('title', MultilingualCharField(_('title'), max_length=255)),
            ('vcard_name', models.CharField(_("vCard Name"), max_length=255, blank=True)),
            ('sort_order', models.IntegerField(_("Sort order"), default=0)),
            ('title_de', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('title_en', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
        )))
        db.send_create_signal('optionset', ['PhoneType'])
        
        # Adding model 'IndividualLocationType'
        db.create_table('optionset_individuallocationtype', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('slug', models.SlugField(unique=True, max_length=255)),
            ('title', MultilingualCharField(_('title'), max_length=255)),
            ('sort_order', models.IntegerField(_("Sort order"), default=0)),
            ('title_de', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('title_en', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
        )))
        db.send_create_signal('optionset', ['IndividualLocationType'])
        
        # Adding model 'EmailType'
        db.create_table('optionset_emailtype', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('slug', models.SlugField(unique=True, max_length=255)),
            ('title', MultilingualCharField(_('title'), max_length=255)),
            ('sort_order', models.IntegerField(_("Sort order"), default=0)),
            ('title_de', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('title_en', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
        )))
        db.send_create_signal('optionset', ['EmailType'])
        
        # Adding model 'InstitutionalLocationType'
        db.create_table('optionset_institutionallocationtype', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('slug', models.SlugField(unique=True, max_length=255)),
            ('title', MultilingualCharField(_('title'), max_length=255)),
            ('sort_order', models.IntegerField(_("Sort order"), default=0)),
            ('title_de', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('title_en', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
        )))
        db.send_create_signal('optionset', ['InstitutionalLocationType'])
        
        # Adding model 'URLType'
        db.create_table('optionset_urltype', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('slug', models.SlugField(unique=True, max_length=255)),
            ('title', MultilingualCharField(_('title'), max_length=255)),
            ('sort_order', models.IntegerField(_("Sort order"), default=0)),
            ('title_de', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('title_en', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
        )))
        db.send_create_signal('optionset', ['URLType'])
        
        # Adding model 'IMType'
        db.create_table('optionset_imtype', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('slug', models.SlugField(unique=True, max_length=255)),
            ('title', MultilingualCharField(_('title'), max_length=255)),
            ('sort_order', models.IntegerField(_("Sort order"), default=0)),
            ('title_de', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('title_en', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
        )))
        db.send_create_signal('optionset', ['IMType'])
        
        # Adding model 'Prefix'
        db.create_table('optionset_prefix', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('slug', models.SlugField(unique=True, max_length=255)),
            ('title', MultilingualCharField(_('title'), max_length=255)),
            ('sort_order', models.IntegerField(_("Sort order"), default=0)),
            ('gender', models.CharField(_("Gender"), blank=True, max_length=32)),
            ('title_de', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('title_en', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
        )))
        db.send_create_signal('optionset', ['Prefix'])
        
        # Adding model 'Salutation'
        db.create_table('optionset_salutation', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('slug', models.SlugField(unique=True, max_length=255)),
            ('title', MultilingualCharField(_('title'), max_length=255)),
            ('template', MultilingualCharField(_('template'), max_length=255)),
            ('sort_order', models.IntegerField(_("Sort Order"), default=0)),
            ('title_de', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('title_en', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('template_de', models.CharField(u'template', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('template_en', models.CharField(u'template', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
        )))
        db.send_create_signal('optionset', ['Salutation'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'PhoneType'
        db.delete_table('optionset_phonetype')
        
        # Deleting model 'IndividualLocationType'
        db.delete_table('optionset_individuallocationtype')
        
        # Deleting model 'EmailType'
        db.delete_table('optionset_emailtype')
        
        # Deleting model 'InstitutionalLocationType'
        db.delete_table('optionset_institutionallocationtype')
        
        # Deleting model 'URLType'
        db.delete_table('optionset_urltype')
        
        # Deleting model 'IMType'
        db.delete_table('optionset_imtype')
        
        # Deleting model 'Prefix'
        db.delete_table('optionset_prefix')
        
        # Deleting model 'Salutation'
        db.delete_table('optionset_salutation')
        
    
    
    models = {
        'optionset.phonetype': {
            'Meta': {'ordering': "['sort_order','title']"},
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('models.IntegerField', ['_("Sort order")'], {'default': '0'}),
            'title': ('MultilingualCharField', ["_('title')"], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'vcard_name': ('models.CharField', ['_("vCard Name")'], {'max_length': '255', 'blank': 'True'})
        },
        'optionset.institutionallocationtype': {
            'Meta': {'ordering': "['sort_order','title']"},
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('models.IntegerField', ['_("Sort order")'], {'default': '0'}),
            'title': ('MultilingualCharField', ["_('title')"], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'optionset.individuallocationtype': {
            'Meta': {'ordering': "['sort_order','title']"},
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('models.IntegerField', ['_("Sort order")'], {'default': '0'}),
            'title': ('MultilingualCharField', ["_('title')"], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'optionset.emailtype': {
            'Meta': {'ordering': "['sort_order','title']"},
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('models.IntegerField', ['_("Sort order")'], {'default': '0'}),
            'title': ('MultilingualCharField', ["_('title')"], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'optionset.urltype': {
            'Meta': {'ordering': "['sort_order','title']"},
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('models.IntegerField', ['_("Sort order")'], {'default': '0'}),
            'title': ('MultilingualCharField', ["_('title')"], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'optionset.imtype': {
            'Meta': {'ordering': "['sort_order','title']"},
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('models.IntegerField', ['_("Sort order")'], {'default': '0'}),
            'title': ('MultilingualCharField', ["_('title')"], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'optionset.prefix': {
            'Meta': {'ordering': "['sort_order','title']"},
            'gender': ('models.CharField', ['_("Gender")'], {'blank': 'True', 'max_length': '32'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('models.IntegerField', ['_("Sort order")'], {'default': '0'}),
            'title': ('MultilingualCharField', ["_('title')"], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'optionset.salutation': {
            'Meta': {'ordering': "['sort_order','title']"},
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('models.IntegerField', ['_("Sort Order")'], {'default': '0'}),
            'template': ('MultilingualCharField', ["_('template')"], {'max_length': '255'}),
            'template_de': ('models.CharField', ["u'template'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'template_en': ('models.CharField', ["u'template'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title': ('MultilingualCharField', ["_('title')"], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['optionset']
