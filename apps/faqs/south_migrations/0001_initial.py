# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from jetson.apps.faqs.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'FaqContainer'
        db.create_table('faqs_faqcontainer', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('creation_date', models.DateTimeField(_("creation date"), editable=False)),
            ('modified_date', models.DateTimeField(_("modified date"), null=True, editable=False)),
            ('content_type', models.ForeignKey(orm['contenttypes.ContentType'], limit_choices_to={}, related_name=None, null=True, blank=True)),
            ('object_id', models.CharField(u'Related object', max_length=255, null=False, blank=True)),
            ('sysname', models.CharField(_("URL Identifier"), max_length=255)),
            ('title', MultilingualCharField(_('title'), max_length=255, blank=True)),
            ('title_de', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('title_en', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
        )))
        db.send_create_signal('faqs', ['FaqContainer'])
        
        # Adding model 'FaqCategory'
        db.create_table('faqs_faqcategory', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('creation_date', models.DateTimeField(_("creation date"), editable=False)),
            ('modified_date', models.DateTimeField(_("modified date"), null=True, editable=False)),
            ('creator', models.ForeignKey(orm['auth.User'], editable=False, related_name="%(class)s_creator", null=True)),
            ('modifier', models.ForeignKey(orm['auth.User'], editable=False, related_name="%(class)s_modifier", null=True)),
            ('sort_order', models.IntegerField(_("sort order"), editable=False, blank=True)),
            ('parent', models.ForeignKey(orm.FaqCategory, related_name="child_set", null=True, blank=True)),
            ('path', models.CharField(_('path'), editable=False, max_length=8192, null=True)),
            ('slug', models.SlugField(unique=True, max_length=255)),
            ('container', models.ForeignKey(orm.FaqContainer)),
            ('title', MultilingualCharField(_('title'), max_length=512)),
            ('short_title', MultilingualCharField(_('short title'), max_length=80)),
            ('description', MultilingualTextField(_('description'), max_length=8192, blank=True)),
            ('children_sort_order_format', models.CharField(_('format for child categories'), default='%02d', max_length=20, null=True, blank=True)),
            ('faqs_on_separate_page', models.BooleanField(_('separate page'), default=False)),
            ('title_de', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=512, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('title_en', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=512, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('description_de', ExtendedTextField(u'description', unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=8192, unique_for_year=None, rel=None, blank=True, null=False, unique_for_date=None, db_tablespace='', db_index=False)),
            ('description_de_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('description_en', ExtendedTextField(u'description', unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=8192, unique_for_year=None, rel=None, blank=True, null=False, unique_for_date=None, db_tablespace='', db_index=False)),
            ('description_en_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('description_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('short_title_de', models.CharField(u'short title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=80, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('short_title_en', models.CharField(u'short title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=80, db_tablespace='', blank=False, unique=False, db_index=False)),
        )))
        db.send_create_signal('faqs', ['FaqCategory'])
        
        # Adding model 'QuestionAnswer'
        db.create_table('faqs_questionanswer', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('creation_date', models.DateTimeField(_("creation date"), editable=False)),
            ('modified_date', models.DateTimeField(_("modified date"), null=True, editable=False)),
            ('creator', models.ForeignKey(orm['auth.User'], editable=False, related_name="%(class)s_creator", null=True)),
            ('modifier', models.ForeignKey(orm['auth.User'], editable=False, related_name="%(class)s_modifier", null=True)),
            ('views', models.IntegerField(_("views"), default=0, editable=False)),
            ('slug', models.SlugField(unique=True, max_length=255)),
            ('category', models.ForeignKey(orm.FaqCategory)),
            ('sort_order', models.IntegerField(_('sort order'))),
            ('question', MultilingualCharField(_('question'), max_length=255)),
            ('answer', MultilingualTextField(_('answer'), max_length=16384)),
            ('question_de', models.CharField(u'question', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('question_en', models.CharField(u'question', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('answer_de', ExtendedTextField(u'answer', unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=16384, unique_for_year=None, rel=None, blank=False, null=False, unique_for_date=None, db_tablespace='', db_index=False)),
            ('answer_de_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('answer_en', ExtendedTextField(u'answer', unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=16384, unique_for_year=None, rel=None, blank=False, null=False, unique_for_date=None, db_tablespace='', db_index=False)),
            ('answer_en_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('answer_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
        )))
        db.send_create_signal('faqs', ['QuestionAnswer'])
        
        # Adding ManyToManyField 'FaqContainer.sites'
        db.create_table('faqs_faqcontainer_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('faqcontainer', models.ForeignKey(orm.FaqContainer, null=False)),
            ('site', models.ForeignKey(orm['sites.Site'], null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'FaqContainer'
        db.delete_table('faqs_faqcontainer')
        
        # Deleting model 'FaqCategory'
        db.delete_table('faqs_faqcategory')
        
        # Deleting model 'QuestionAnswer'
        db.delete_table('faqs_questionanswer')
        
        # Dropping ManyToManyField 'FaqContainer.sites'
        db.delete_table('faqs_faqcontainer_sites')
        
    
    
    models = {
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'db_table': "'django_site'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'faqs.faqcontainer': {
            'Meta': {'ordering': "('title',)"},
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'limit_choices_to': '{}', 'related_name': 'None', 'null': 'True', 'blank': 'True'}),
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'editable': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('models.DateTimeField', ['_("modified date")'], {'null': 'True', 'editable': 'False'}),
            'object_id': ('models.CharField', ["u'Related object'"], {'max_length': '255', 'null': 'False', 'blank': 'True'}),
            'sites': ('models.ManyToManyField', ["orm['sites.Site']"], {'null': 'True', 'blank': 'True'}),
            'sysname': ('models.CharField', ['_("URL Identifier")'], {'max_length': '255'}),
            'title': ('MultilingualCharField', ["_('title')"], {'max_length': '255', 'blank': 'True'}),
            'title_de': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        'faqs.faqcategory': {
            'children_sort_order_format': ('models.CharField', ["_('format for child categories')"], {'default': "'%02d'", 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'container': ('models.ForeignKey', ["orm['faqs.FaqContainer']"], {}),
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'editable': 'False'}),
            'creator': ('models.ForeignKey', ["orm['auth.User']"], {'editable': 'False', 'related_name': '"%(class)s_creator"', 'null': 'True'}),
            'description': ('MultilingualTextField', ["_('description')"], {'max_length': '8192', 'blank': 'True'}),
            'description_de': ('ExtendedTextField', ["u'description'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'max_length': '8192', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('ExtendedTextField', ["u'description'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'max_length': '8192', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'faqs_on_separate_page': ('models.BooleanField', ["_('separate page')"], {'default': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('models.DateTimeField', ['_("modified date")'], {'null': 'True', 'editable': 'False'}),
            'modifier': ('models.ForeignKey', ["orm['auth.User']"], {'editable': 'False', 'related_name': '"%(class)s_modifier"', 'null': 'True'}),
            'parent': ('models.ForeignKey', ["orm['faqs.FaqCategory']"], {'related_name': '"child_set"', 'null': 'True', 'blank': 'True'}),
            'path': ('models.CharField', ["_('path')"], {'editable': 'False', 'max_length': '8192', 'null': 'True'}),
            'short_title': ('MultilingualCharField', ["_('short title')"], {'max_length': '80'}),
            'short_title_de': ('models.CharField', ["u'short title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '80', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'short_title_en': ('models.CharField', ["u'short title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '80', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('models.IntegerField', ['_("sort order")'], {'editable': 'False', 'blank': 'True'}),
            'title': ('MultilingualCharField', ["_('title')"], {'max_length': '512'}),
            'title_de': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '512', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '512', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'faqs.questionanswer': {
            'Meta': {'ordering': "['category']"},
            'answer': ('MultilingualTextField', ["_('answer')"], {'max_length': '16384'}),
            'answer_de': ('ExtendedTextField', ["u'answer'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'max_length': '16384', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'False', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'answer_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'answer_en': ('ExtendedTextField', ["u'answer'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'max_length': '16384', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'False', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'answer_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'answer_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'category': ('models.ForeignKey', ["orm['faqs.FaqCategory']"], {}),
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'editable': 'False'}),
            'creator': ('models.ForeignKey', ["orm['auth.User']"], {'editable': 'False', 'related_name': '"%(class)s_creator"', 'null': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('models.DateTimeField', ['_("modified date")'], {'null': 'True', 'editable': 'False'}),
            'modifier': ('models.ForeignKey', ["orm['auth.User']"], {'editable': 'False', 'related_name': '"%(class)s_modifier"', 'null': 'True'}),
            'question': ('MultilingualCharField', ["_('question')"], {'max_length': '255'}),
            'question_de': ('models.CharField', ["u'question'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'question_en': ('models.CharField', ["u'question'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('models.IntegerField', ["_('sort order')"], {}),
            'views': ('models.IntegerField', ['_("views")'], {'default': '0', 'editable': 'False'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['faqs']
