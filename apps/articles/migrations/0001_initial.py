# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from jetson.apps.articles.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Article'
        db.create_table('articles_article', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('creation_date', models.DateTimeField(_("creation date"), editable=False)),
            ('modified_date', models.DateTimeField(_("modified date"), null=True, editable=False)),
            ('author', models.ForeignKey(orm['auth.User'], related_name="%(class)s_author", null=True, blank=True)),
            ('published_from', models.DateTimeField(_("publishing date"), null=True, blank=True)),
            ('published_till', models.DateTimeField(_("published until"), null=True, blank=True)),
            ('status', models.SmallIntegerField(_("status"), default=0)),
            ('views', models.IntegerField(_("views"), default=0, editable=False)),
            ('slug', models.SlugField(unique=True, max_length=255)),
            ('article_type', models.ForeignKey(orm['structure.Term'], limit_choices_to={'vocabulary__sysname':'basics_article_types'})),
            ('title', MultilingualCharField(_('title'), max_length=255)),
            ('title_de', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('title_en', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('subtitle', MultilingualCharField(_('subtitle'), max_length=255, blank=True)),
            ('subtitle_de', models.CharField(u'subtitle', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('subtitle_en', models.CharField(u'subtitle', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('description', MultilingualTextField(_('summary'), blank=True)),
            ('description_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('description_de', ExtendedTextField(u'summary', unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, unique_for_year=None, rel=None, blank=True, null=False, unique_for_date=None, db_tablespace='', db_index=False)),
            ('description_de_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('description_en', ExtendedTextField(u'summary', unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, unique_for_year=None, rel=None, blank=True, null=False, unique_for_date=None, db_tablespace='', db_index=False)),
            ('description_en_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('content', MultilingualTextField(_('entry'))),
            ('content_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('content_de', ExtendedTextField(u'entry', unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, unique_for_year=None, rel=None, blank=False, null=False, unique_for_date=None, db_tablespace='', db_index=False)),
            ('content_de_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('content_en', ExtendedTextField(u'entry', unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, unique_for_year=None, rel=None, blank=False, null=False, unique_for_date=None, db_tablespace='', db_index=False)),
            ('content_en_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('image_title', MultilingualCharField(_('image title'), max_length=50, blank=True)),
            ('image_title_de', models.CharField(u'image title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=50, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('image_title_en', models.CharField(u'image title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=50, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('image_description', MultilingualTextField(_('image description'), blank=True)),
            ('image_description_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('image_description_de', ExtendedTextField(u'image description', unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, unique_for_year=None, rel=None, blank=True, null=False, unique_for_date=None, db_tablespace='', db_index=False)),
            ('image_description_de_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('image_description_en', ExtendedTextField(u'image description', unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, unique_for_year=None, rel=None, blank=True, null=False, unique_for_date=None, db_tablespace='', db_index=False)),
            ('image_description_en_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('image', FileBrowseField(_('overview image'), extensions=['.jpg','.jpeg','.gif','.png','.tif','.tiff'], max_length=255, directory="/articles/", blank=True)),
            ('is_featured', models.BooleanField(_("Featured"), default=False)),
        )))
        db.send_create_signal('articles', ['Article'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Article'
        db.delete_table('articles_article')
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'articles.article': {
            'article_type': ('models.ForeignKey', ["orm['structure.Term']"], {'limit_choices_to': "{'vocabulary__sysname':'basics_article_types'}"}),
            'author': ('models.ForeignKey', ["orm['auth.User']"], {'related_name': '"%(class)s_author"', 'null': 'True', 'blank': 'True'}),
            'content': ('MultilingualTextField', ["_('entry')"], {}),
            'content_de': ('ExtendedTextField', ["u'entry'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'False', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'content_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'content_en': ('ExtendedTextField', ["u'entry'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'False', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'content_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'content_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'editable': 'False'}),
            'description': ('MultilingualTextField', ["_('summary')"], {'blank': 'True'}),
            'description_de': ('ExtendedTextField', ["u'summary'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('ExtendedTextField', ["u'summary'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'image': ('FileBrowseField', ["_('overview image')"], {'extensions': "['.jpg','.jpeg','.gif','.png','.tif','.tiff']", 'max_length': '255', 'directory': '"/articles/"', 'blank': 'True'}),
            'image_description': ('MultilingualTextField', ["_('image description')"], {'blank': 'True'}),
            'image_description_de': ('ExtendedTextField', ["u'image description'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'image_description_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'image_description_en': ('ExtendedTextField', ["u'image description'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'image_description_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'image_description_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'image_title': ('MultilingualCharField', ["_('image title')"], {'max_length': '50', 'blank': 'True'}),
            'image_title_de': ('models.CharField', ["u'image title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '50', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'image_title_en': ('models.CharField', ["u'image title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '50', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'is_featured': ('models.BooleanField', ['_("Featured")'], {'default': 'False'}),
            'modified_date': ('models.DateTimeField', ['_("modified date")'], {'null': 'True', 'editable': 'False'}),
            'published_from': ('models.DateTimeField', ['_("publishing date")'], {'null': 'True', 'blank': 'True'}),
            'published_till': ('models.DateTimeField', ['_("published until")'], {'null': 'True', 'blank': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'status': ('models.SmallIntegerField', ['_("status")'], {'default': '0'}),
            'subtitle': ('MultilingualCharField', ["_('subtitle')"], {'max_length': '255', 'blank': 'True'}),
            'subtitle_de': ('models.CharField', ["u'subtitle'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'subtitle_en': ('models.CharField', ["u'subtitle'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title': ('MultilingualCharField', ["_('title')"], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'views': ('models.IntegerField', ['_("views")'], {'default': '0', 'editable': 'False'})
        },
        'structure.term': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['articles']
