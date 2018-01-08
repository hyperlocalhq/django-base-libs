# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from jetson.apps.contact_form.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'ContactFormCategory'
        db.create_table('contact_form_contactformcategory', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('site', models.ForeignKey(orm['sites.Site'], null=True, blank=True)),
            ('slug', models.SlugField(unique=True, max_length=255)),
            ('title', MultilingualCharField(_('title'), max_length=255)),
            ('recipient_emails', PlainTextModelField(_("Recipient email(s)"), null=True, blank=True)),
            ('auto_answer_template', models.ForeignKey(orm['mailing.EmailTemplate'], null=True, blank=True)),
            ('sort_order', models.IntegerField(_("Sort order"), default=0)),
            ('title_de', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('title_en', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
        )))
        db.send_create_signal('contact_form', ['ContactFormCategory'])
        
        # Adding ManyToManyField 'ContactFormCategory.recipients'
        db.create_table('contact_form_contactformcategory_recipients', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('contactformcategory', models.ForeignKey(orm.ContactFormCategory, null=False)),
            ('user', models.ForeignKey(orm['auth.User'], null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'ContactFormCategory'
        db.delete_table('contact_form_contactformcategory')
        
        # Dropping ManyToManyField 'ContactFormCategory.recipients'
        db.delete_table('contact_form_contactformcategory_recipients')
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'db_table': "'django_site'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'mailing.emailtemplate': {
            'Meta': {'ordering': "['-timestamp','name']"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'contact_form.contactformcategory': {
            'Meta': {'ordering': "['sort_order','title']"},
            'auto_answer_template': ('models.ForeignKey', ["orm['mailing.EmailTemplate']"], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'recipient_emails': ('PlainTextModelField', ['_("Recipient email(s)")'], {'null': 'True', 'blank': 'True'}),
            'recipients': ('models.ManyToManyField', ["orm['auth.User']"], {'null': 'True', 'blank': 'True'}),
            'site': ('models.ForeignKey', ["orm['sites.Site']"], {'null': 'True', 'blank': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('models.IntegerField', ['_("Sort order")'], {'default': '0'}),
            'title': ('MultilingualCharField', ["_('title')"], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['contact_form']
