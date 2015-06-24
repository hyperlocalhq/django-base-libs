# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from jetson.apps.flatpages.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'FlatPage'
        db.create_table('flatpages_flatpage', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('creation_date', models.DateTimeField(_("creation date"), editable=False)),
            ('modified_date', models.DateTimeField(_("modified date"), null=True, editable=False)),
            ('creator', models.ForeignKey(orm['auth.User'], editable=False, related_name="%(class)s_creator", null=True)),
            ('modifier', models.ForeignKey(orm['auth.User'], editable=False, related_name="%(class)s_modifier", null=True)),
            ('author', models.ForeignKey(orm['auth.User'], related_name="%(class)s_author", null=True, blank=True)),
            ('published_from', models.DateTimeField(_("publishing date"), null=True, blank=True)),
            ('published_till', models.DateTimeField(_("published until"), null=True, blank=True)),
            ('status', models.SmallIntegerField(_("status"), default=0)),
            ('title', MultilingualCharField(_('title'), max_length=255)),
            ('subtitle', MultilingualCharField(_('subtitle'), max_length=255, blank=True)),
            ('short_title', MultilingualCharField(_('short title'), max_length=32, blank=True)),
            ('content', MultilingualTextField(_('content'), blank=True)),
            ('url', models.CharField(_('URL'), max_length=100, blank=True)),
            ('image', FileBrowseField(_('image'), extensions=['.jpg','.jpeg','.gif','.png','.tif','.tiff'], max_length=255, blank=True)),
            ('image_title', MultilingualCharField(_('image title'), max_length=50, blank=True)),
            ('image_description', MultilingualTextField(_('image description'), blank=True)),
            ('enable_comments', models.BooleanField(_('enable comments'), default=False)),
            ('template_name', models.CharField(_('template name'), max_length=70, blank=True)),
            ('registration_required', models.BooleanField(_('registration required'), default=False)),
            ('title_de', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('title_en', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('subtitle_de', models.CharField(u'subtitle', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('subtitle_en', models.CharField(u'subtitle', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('short_title_de', models.CharField(u'short title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=32, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('short_title_en', models.CharField(u'short title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=32, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('content_de', ExtendedTextField(u'content', unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, unique_for_year=None, rel=None, blank=True, null=False, unique_for_date=None, db_tablespace='', db_index=False)),
            ('content_de_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('content_en', ExtendedTextField(u'content', unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, unique_for_year=None, rel=None, blank=True, null=False, unique_for_date=None, db_tablespace='', db_index=False)),
            ('content_en_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('content_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('image_title_de', models.CharField(u'image title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=50, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('image_title_en', models.CharField(u'image title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=50, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('image_description_de', ExtendedTextField(u'image description', unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, unique_for_year=None, rel=None, blank=True, null=False, unique_for_date=None, db_tablespace='', db_index=False)),
            ('image_description_de_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('image_description_en', ExtendedTextField(u'image description', unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, unique_for_year=None, rel=None, blank=True, null=False, unique_for_date=None, db_tablespace='', db_index=False)),
            ('image_description_en_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('image_description_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
        )))
        db.send_create_signal('flatpages', ['FlatPage'])
        
        # Adding ManyToManyField 'FlatPage.sites'
        db.create_table('flatpages_flatpage_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('flatpage', models.ForeignKey(orm.FlatPage, null=False)),
            ('site', models.ForeignKey(orm['sites.Site'], null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'FlatPage'
        db.delete_table('flatpages_flatpage')
        
        # Dropping ManyToManyField 'FlatPage.sites'
        db.delete_table('flatpages_flatpage_sites')
        
    
    
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
        'flatpages.flatpage': {
            'author': ('models.ForeignKey', ["orm['auth.User']"], {'related_name': '"%(class)s_author"', 'null': 'True', 'blank': 'True'}),
            'content': ('MultilingualTextField', ["_('content')"], {'blank': 'True'}),
            'content_de': ('ExtendedTextField', ["u'content'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'content_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'content_en': ('ExtendedTextField', ["u'content'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'content_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'content_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'editable': 'False'}),
            'creator': ('models.ForeignKey', ["orm['auth.User']"], {'editable': 'False', 'related_name': '"%(class)s_creator"', 'null': 'True'}),
            'enable_comments': ('models.BooleanField', ["_('enable comments')"], {'default': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'image': ('FileBrowseField', ["_('image')"], {'extensions': "['.jpg','.jpeg','.gif','.png','.tif','.tiff']", 'max_length': '255', 'blank': 'True'}),
            'image_description': ('MultilingualTextField', ["_('image description')"], {'blank': 'True'}),
            'image_description_de': ('ExtendedTextField', ["u'image description'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'image_description_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'image_description_en': ('ExtendedTextField', ["u'image description'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'image_description_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'image_description_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'image_title': ('MultilingualCharField', ["_('image title')"], {'max_length': '50', 'blank': 'True'}),
            'image_title_de': ('models.CharField', ["u'image title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '50', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'image_title_en': ('models.CharField', ["u'image title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '50', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'modified_date': ('models.DateTimeField', ['_("modified date")'], {'null': 'True', 'editable': 'False'}),
            'modifier': ('models.ForeignKey', ["orm['auth.User']"], {'editable': 'False', 'related_name': '"%(class)s_modifier"', 'null': 'True'}),
            'published_from': ('models.DateTimeField', ['_("publishing date")'], {'null': 'True', 'blank': 'True'}),
            'published_till': ('models.DateTimeField', ['_("published until")'], {'null': 'True', 'blank': 'True'}),
            'registration_required': ('models.BooleanField', ["_('registration required')"], {'default': 'False'}),
            'short_title': ('MultilingualCharField', ["_('short title')"], {'max_length': '32', 'blank': 'True'}),
            'short_title_de': ('models.CharField', ["u'short title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '32', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'short_title_en': ('models.CharField', ["u'short title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '32', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'sites': ('models.ManyToManyField', ["orm['sites.Site']"], {}),
            'status': ('models.SmallIntegerField', ['_("status")'], {'default': '0'}),
            'subtitle': ('MultilingualCharField', ["_('subtitle')"], {'max_length': '255', 'blank': 'True'}),
            'subtitle_de': ('models.CharField', ["u'subtitle'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'subtitle_en': ('models.CharField', ["u'subtitle'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'template_name': ('models.CharField', ["_('template name')"], {'max_length': '70', 'blank': 'True'}),
            'title': ('MultilingualCharField', ["_('title')"], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'url': ('models.CharField', ["_('URL')"], {'max_length': '100', 'blank': 'True'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['flatpages']
