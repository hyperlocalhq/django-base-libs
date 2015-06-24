# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from jetson.apps.forum.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Forum'
        db.create_table('forum_forum', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('creation_date', models.DateTimeField(_("creation date"), editable=False)),
            ('modified_date', models.DateTimeField(_("modified date"), null=True, editable=False)),
            ('creator', models.ForeignKey(orm['auth.User'], editable=False, related_name="%(class)s_creator", null=True)),
            ('modifier', models.ForeignKey(orm['auth.User'], editable=False, related_name="%(class)s_modifier", null=True)),
            ('sort_order', models.IntegerField(_("sort order"), editable=False, blank=True)),
            ('parent', models.ForeignKey(orm.Forum, related_name="child_set", null=True, blank=True)),
            ('path', models.CharField(_('path'), editable=False, max_length=8192, null=True)),
            ('slug', models.SlugField(unique=True, max_length=255)),
            ('container', models.ForeignKey(orm.ForumContainer)),
            ('title', models.CharField(_('title'), max_length=512)),
            ('short_title', models.CharField(_('short title'), max_length=32, blank=True)),
            ('description', ExtendedTextField(_('description'), blank=True)),
            ('status', models.IntegerField(_("status"), default=0)),
            ('description_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
        )))
        db.send_create_signal('forum', ['Forum'])
        
        # Adding model 'ForumContainer'
        db.create_table('forum_forumcontainer', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('creation_date', models.DateTimeField(_("creation date"), editable=False)),
            ('modified_date', models.DateTimeField(_("modified date"), null=True, editable=False)),
            ('content_type', models.ForeignKey(orm['contenttypes.ContentType'], limit_choices_to={}, related_name=None, null=True, blank=True)),
            ('object_id', models.CharField(u'Related object', max_length=255, null=False, blank=True)),
            ('sysname', models.CharField(_("URL Identifier"), max_length=255)),
            ('title', MultilingualCharField(_('title'), max_length=255, blank=True)),
            ('allow_bumping', models.BooleanField(_("allow bumping"), default=False)),
            ('max_level', models.IntegerField(_("max nesting level"), default=1)),
            ('title_de', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('title_en', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
        )))
        db.send_create_signal('forum', ['ForumContainer'])
        
        # Adding model 'ForumReply'
        db.create_table('forum_forumreply', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('creation_date', models.DateTimeField(_("creation date"), editable=False)),
            ('modified_date', models.DateTimeField(_("modified date"), null=True, editable=False)),
            ('creator', models.ForeignKey(orm['auth.User'], editable=False, related_name="%(class)s_creator", null=True)),
            ('modifier', models.ForeignKey(orm['auth.User'], editable=False, related_name="%(class)s_modifier", null=True)),
            ('sort_order', models.IntegerField(_("sort order"), editable=False, blank=True)),
            ('parent', models.ForeignKey(orm.ForumReply, related_name="child_set", null=True, blank=True)),
            ('path', models.CharField(_('path'), editable=False, max_length=8192, null=True)),
            ('slug', models.SlugField(unique=True, max_length=255)),
            ('thread', models.ForeignKey(orm.ForumThread)),
            ('subject', models.CharField(_('subject'), max_length=255, blank=True)),
            ('message', ExtendedTextField(_('message'))),
            ('message_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
        )))
        db.send_create_signal('forum', ['ForumReply'])
        
        # Adding model 'ForumThread'
        db.create_table('forum_forumthread', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('creation_date', models.DateTimeField(_("creation date"), editable=False)),
            ('modified_date', models.DateTimeField(_("modified date"), null=True, editable=False)),
            ('creator', models.ForeignKey(orm['auth.User'], editable=False, related_name="%(class)s_creator", null=True)),
            ('modifier', models.ForeignKey(orm['auth.User'], editable=False, related_name="%(class)s_modifier", null=True)),
            ('views', models.IntegerField(_("views"), default=0, editable=False)),
            ('slug', models.SlugField(unique=True, max_length=255)),
            ('forum', models.ForeignKey(orm.Forum)),
            ('subject', models.CharField(_('subject'), max_length=255)),
            ('message', ExtendedTextField(_('message'))),
            ('is_sticky', models.BooleanField(_("is sticky"), default=False)),
            ('status', models.IntegerField(_("status"), default=0)),
            ('message_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
        )))
        db.send_create_signal('forum', ['ForumThread'])
        
        # Adding ManyToManyField 'ForumContainer.sites'
        db.create_table('forum_forumcontainer_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('forumcontainer', models.ForeignKey(orm.ForumContainer, null=False)),
            ('site', models.ForeignKey(orm['sites.Site'], null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Forum'
        db.delete_table('forum_forum')
        
        # Deleting model 'ForumContainer'
        db.delete_table('forum_forumcontainer')
        
        # Deleting model 'ForumReply'
        db.delete_table('forum_forumreply')
        
        # Deleting model 'ForumThread'
        db.delete_table('forum_forumthread')
        
        # Dropping ManyToManyField 'ForumContainer.sites'
        db.delete_table('forum_forumcontainer_sites')
        
    
    
    models = {
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'db_table': "'django_site'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'forum.forumcontainer': {
            'Meta': {'ordering': "('title',)"},
            'allow_bumping': ('models.BooleanField', ['_("allow bumping")'], {'default': 'False'}),
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'limit_choices_to': '{}', 'related_name': 'None', 'null': 'True', 'blank': 'True'}),
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'editable': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'max_level': ('models.IntegerField', ['_("max nesting level")'], {'default': '1'}),
            'modified_date': ('models.DateTimeField', ['_("modified date")'], {'null': 'True', 'editable': 'False'}),
            'object_id': ('models.CharField', ["u'Related object'"], {'max_length': '255', 'null': 'False', 'blank': 'True'}),
            'sites': ('models.ManyToManyField', ["orm['sites.Site']"], {'null': 'True', 'blank': 'True'}),
            'sysname': ('models.CharField', ['_("URL Identifier")'], {'max_length': '255'}),
            'title': ('MultilingualCharField', ["_('title')"], {'max_length': '255', 'blank': 'True'}),
            'title_de': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'forum.forum': {
            'container': ('models.ForeignKey', ["orm['forum.ForumContainer']"], {}),
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'editable': 'False'}),
            'creator': ('models.ForeignKey', ["orm['auth.User']"], {'editable': 'False', 'related_name': '"%(class)s_creator"', 'null': 'True'}),
            'description': ('ExtendedTextField', ["_('description')"], {'blank': 'True'}),
            'description_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('models.DateTimeField', ['_("modified date")'], {'null': 'True', 'editable': 'False'}),
            'modifier': ('models.ForeignKey', ["orm['auth.User']"], {'editable': 'False', 'related_name': '"%(class)s_modifier"', 'null': 'True'}),
            'parent': ('models.ForeignKey', ["orm['forum.Forum']"], {'related_name': '"child_set"', 'null': 'True', 'blank': 'True'}),
            'path': ('models.CharField', ["_('path')"], {'editable': 'False', 'max_length': '8192', 'null': 'True'}),
            'short_title': ('models.CharField', ["_('short title')"], {'max_length': '32', 'blank': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('models.IntegerField', ['_("sort order")'], {'editable': 'False', 'blank': 'True'}),
            'status': ('models.IntegerField', ['_("status")'], {'default': '0'}),
            'title': ('models.CharField', ["_('title')"], {'max_length': '512'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'forum.forumthread': {
            'Meta': {'ordering': "['forum','-is_sticky','creation_date']"},
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'editable': 'False'}),
            'creator': ('models.ForeignKey', ["orm['auth.User']"], {'editable': 'False', 'related_name': '"%(class)s_creator"', 'null': 'True'}),
            'forum': ('models.ForeignKey', ["orm['forum.Forum']"], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'is_sticky': ('models.BooleanField', ['_("is sticky")'], {'default': 'False'}),
            'message': ('ExtendedTextField', ["_('message')"], {}),
            'message_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'modified_date': ('models.DateTimeField', ['_("modified date")'], {'null': 'True', 'editable': 'False'}),
            'modifier': ('models.ForeignKey', ["orm['auth.User']"], {'editable': 'False', 'related_name': '"%(class)s_modifier"', 'null': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'status': ('models.IntegerField', ['_("status")'], {'default': '0'}),
            'subject': ('models.CharField', ["_('subject')"], {'max_length': '255'}),
            'views': ('models.IntegerField', ['_("views")'], {'default': '0', 'editable': 'False'})
        },
        'forum.forumreply': {
            'Meta': {'ordering': "['thread','creation_date']"},
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'editable': 'False'}),
            'creator': ('models.ForeignKey', ["orm['auth.User']"], {'editable': 'False', 'related_name': '"%(class)s_creator"', 'null': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'message': ('ExtendedTextField', ["_('message')"], {}),
            'message_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'modified_date': ('models.DateTimeField', ['_("modified date")'], {'null': 'True', 'editable': 'False'}),
            'modifier': ('models.ForeignKey', ["orm['auth.User']"], {'editable': 'False', 'related_name': '"%(class)s_modifier"', 'null': 'True'}),
            'parent': ('models.ForeignKey', ["orm['forum.ForumReply']"], {'related_name': '"child_set"', 'null': 'True', 'blank': 'True'}),
            'path': ('models.CharField', ["_('path')"], {'editable': 'False', 'max_length': '8192', 'null': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('models.IntegerField', ['_("sort order")'], {'editable': 'False', 'blank': 'True'}),
            'subject': ('models.CharField', ["_('subject')"], {'max_length': '255', 'blank': 'True'}),
            'thread': ('models.ForeignKey', ["orm['forum.ForumThread']"], {})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['forum']
