# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Deleting field 'forum.path'
        db.delete_column('forum_forum', 'path')

        # Adding field 'Forum.lft'
        db.add_column('forum_forum', 'lft', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True), keep_default=False)

        # Adding field 'Forum.rght'
        db.add_column('forum_forum', 'rght', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True), keep_default=False)

        # Adding field 'Forum.tree_id'
        db.add_column('forum_forum', 'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True), keep_default=False)

        # Adding field 'Forum.level'
        db.add_column('forum_forum', 'level', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True), keep_default=False)

        # Changing field 'Forum.status'
        db.alter_column('forum_forum', 'status', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Forum.modified_date'
        db.alter_column('forum_forum', 'modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Forum.container'
        db.alter_column('forum_forum', 'container_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forum.ForumContainer']))

        # Changing field 'Forum.description'
        db.alter_column('forum_forum', 'description', self.gf('base_libs.models.fields.ExtendedTextField')())

        # Changing field 'Forum.parent'
        db.alter_column('forum_forum', 'parent_id', self.gf('mptt.fields.TreeForeignKey')(null=True, to=orm['forum.Forum']))

        # Changing field 'Forum.creator'
        db.alter_column('forum_forum', 'creator_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'Forum.title'
        db.alter_column('forum_forum', 'title', self.gf('django.db.models.fields.CharField')(max_length=512))

        # Changing field 'Forum.short_title'
        db.alter_column('forum_forum', 'short_title', self.gf('django.db.models.fields.CharField')(max_length=32))

        # Changing field 'Forum.creation_date'
        db.alter_column('forum_forum', 'creation_date', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Forum.sort_order'
        db.alter_column('forum_forum', 'sort_order', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Forum.modifier'
        db.alter_column('forum_forum', 'modifier_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'ForumContainer.modified_date'
        db.alter_column('forum_forumcontainer', 'modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'ForumContainer.title'
        db.alter_column('forum_forumcontainer', 'title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True))

        # Changing field 'ForumContainer.max_level'
        db.alter_column('forum_forumcontainer', 'max_level', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'ForumContainer.allow_bumping'
        db.alter_column('forum_forumcontainer', 'allow_bumping', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'ForumContainer.creation_date'
        db.alter_column('forum_forumcontainer', 'creation_date', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'ForumContainer.sysname'
        db.alter_column('forum_forumcontainer', 'sysname', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'ForumContainer.content_type'
        db.alter_column('forum_forumcontainer', 'content_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True))

        # Deleting field 'forumreply.path'
        db.delete_column('forum_forumreply', 'path')

        # Adding field 'ForumReply.lft'
        db.add_column('forum_forumreply', 'lft', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True), keep_default=False)

        # Adding field 'ForumReply.rght'
        db.add_column('forum_forumreply', 'rght', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True), keep_default=False)

        # Adding field 'ForumReply.tree_id'
        db.add_column('forum_forumreply', 'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True), keep_default=False)

        # Adding field 'ForumReply.level'
        db.add_column('forum_forumreply', 'level', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True), keep_default=False)

        # Changing field 'ForumReply.modified_date'
        db.alter_column('forum_forumreply', 'modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'ForumReply.thread'
        db.alter_column('forum_forumreply', 'thread_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forum.ForumThread']))

        # Changing field 'ForumReply.parent'
        db.alter_column('forum_forumreply', 'parent_id', self.gf('mptt.fields.TreeForeignKey')(null=True, to=orm['forum.ForumReply']))

        # Changing field 'ForumReply.creator'
        db.alter_column('forum_forumreply', 'creator_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'ForumReply.creation_date'
        db.alter_column('forum_forumreply', 'creation_date', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'ForumReply.sort_order'
        db.alter_column('forum_forumreply', 'sort_order', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'ForumReply.message'
        db.alter_column('forum_forumreply', 'message', self.gf('base_libs.models.fields.ExtendedTextField')())

        # Changing field 'ForumReply.modifier'
        db.alter_column('forum_forumreply', 'modifier_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'ForumReply.subject'
        db.alter_column('forum_forumreply', 'subject', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'ForumThread.status'
        db.alter_column('forum_forumthread', 'status', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'ForumThread.modified_date'
        db.alter_column('forum_forumthread', 'modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'ForumThread.forum'
        db.alter_column('forum_forumthread', 'forum_id', self.gf('mptt.fields.TreeForeignKey')(to=orm['forum.Forum']))

        # Changing field 'ForumThread.is_sticky'
        db.alter_column('forum_forumthread', 'is_sticky', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'ForumThread.views'
        db.alter_column('forum_forumthread', 'views', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'ForumThread.creation_date'
        db.alter_column('forum_forumthread', 'creation_date', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'ForumThread.message'
        db.alter_column('forum_forumthread', 'message', self.gf('base_libs.models.fields.ExtendedTextField')())

        # Changing field 'ForumThread.modifier'
        db.alter_column('forum_forumthread', 'modifier_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'ForumThread.creator'
        db.alter_column('forum_forumthread', 'creator_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'ForumThread.subject'
        db.alter_column('forum_forumthread', 'subject', self.gf('django.db.models.fields.CharField')(max_length=255))
    
    
    def backwards(self, orm):
        # Adding field 'forum.path'
        db.add_column('forum_forum', 'path', self.gf('models.CharField')(_('path'), null=True, max_length=8192, editable=False), keep_default=False)

        # Deleting field 'Forum.lft'
        db.delete_column('forum_forum', 'lft')

        # Deleting field 'Forum.rght'
        db.delete_column('forum_forum', 'rght')

        # Deleting field 'Forum.tree_id'
        db.delete_column('forum_forum', 'tree_id')

        # Deleting field 'Forum.level'
        db.delete_column('forum_forum', 'level')

        # Changing field 'Forum.status'
        db.alter_column('forum_forum', 'status', self.gf('models.IntegerField')(_("status")))

        # Changing field 'Forum.modified_date'
        db.alter_column('forum_forum', 'modified_date', self.gf('models.DateTimeField')(_("modified date"), null=True, editable=False))

        # Changing field 'Forum.container'
        db.alter_column('forum_forum', 'container_id', self.gf('models.ForeignKey')(orm['forum.ForumContainer']))

        # Changing field 'Forum.description'
        db.alter_column('forum_forum', 'description', self.gf('ExtendedTextField')(_('description')))

        # Changing field 'Forum.parent'
        db.alter_column('forum_forum', 'parent_id', self.gf('models.ForeignKey')(orm['forum.Forum'], null=True))

        # Changing field 'Forum.creator'
        db.alter_column('forum_forum', 'creator_id', self.gf('models.ForeignKey')(orm['auth.User'], null=True, editable=False))

        # Changing field 'Forum.title'
        db.alter_column('forum_forum', 'title', self.gf('models.CharField')(_('title'), max_length=512))

        # Changing field 'Forum.short_title'
        db.alter_column('forum_forum', 'short_title', self.gf('models.CharField')(_('short title'), max_length=32))

        # Changing field 'Forum.creation_date'
        db.alter_column('forum_forum', 'creation_date', self.gf('models.DateTimeField')(_("creation date"), editable=False))

        # Changing field 'Forum.sort_order'
        db.alter_column('forum_forum', 'sort_order', self.gf('models.IntegerField')(_("sort order"), editable=False))

        # Changing field 'Forum.modifier'
        db.alter_column('forum_forum', 'modifier_id', self.gf('models.ForeignKey')(orm['auth.User'], null=True, editable=False))

        # Changing field 'ForumContainer.modified_date'
        db.alter_column('forum_forumcontainer', 'modified_date', self.gf('models.DateTimeField')(_("modified date"), null=True, editable=False))

        # Changing field 'ForumContainer.title'
        db.alter_column('forum_forumcontainer', 'title', self.gf('MultilingualCharField')(_('title'), max_length=255))

        # Changing field 'ForumContainer.max_level'
        db.alter_column('forum_forumcontainer', 'max_level', self.gf('models.IntegerField')(_("max nesting level")))

        # Changing field 'ForumContainer.allow_bumping'
        db.alter_column('forum_forumcontainer', 'allow_bumping', self.gf('models.BooleanField')(_("allow bumping")))

        # Changing field 'ForumContainer.creation_date'
        db.alter_column('forum_forumcontainer', 'creation_date', self.gf('models.DateTimeField')(_("creation date"), editable=False))

        # Changing field 'ForumContainer.sysname'
        db.alter_column('forum_forumcontainer', 'sysname', self.gf('models.CharField')(_("URL Identifier"), max_length=255))

        # Changing field 'ForumContainer.content_type'
        db.alter_column('forum_forumcontainer', 'content_type_id', self.gf('models.ForeignKey')(orm['contenttypes.ContentType'], limit_choices_to={}, null=True))

        # Adding field 'forumreply.path'
        db.add_column('forum_forumreply', 'path', self.gf('models.CharField')(_('path'), null=True, max_length=8192, editable=False), keep_default=False)

        # Deleting field 'ForumReply.lft'
        db.delete_column('forum_forumreply', 'lft')

        # Deleting field 'ForumReply.rght'
        db.delete_column('forum_forumreply', 'rght')

        # Deleting field 'ForumReply.tree_id'
        db.delete_column('forum_forumreply', 'tree_id')

        # Deleting field 'ForumReply.level'
        db.delete_column('forum_forumreply', 'level')

        # Changing field 'ForumReply.modified_date'
        db.alter_column('forum_forumreply', 'modified_date', self.gf('models.DateTimeField')(_("modified date"), null=True, editable=False))

        # Changing field 'ForumReply.thread'
        db.alter_column('forum_forumreply', 'thread_id', self.gf('models.ForeignKey')(orm['forum.ForumThread']))

        # Changing field 'ForumReply.parent'
        db.alter_column('forum_forumreply', 'parent_id', self.gf('models.ForeignKey')(orm['forum.ForumReply'], null=True))

        # Changing field 'ForumReply.creator'
        db.alter_column('forum_forumreply', 'creator_id', self.gf('models.ForeignKey')(orm['auth.User'], null=True, editable=False))

        # Changing field 'ForumReply.creation_date'
        db.alter_column('forum_forumreply', 'creation_date', self.gf('models.DateTimeField')(_("creation date"), editable=False))

        # Changing field 'ForumReply.sort_order'
        db.alter_column('forum_forumreply', 'sort_order', self.gf('models.IntegerField')(_("sort order"), editable=False))

        # Changing field 'ForumReply.message'
        db.alter_column('forum_forumreply', 'message', self.gf('ExtendedTextField')(_('message')))

        # Changing field 'ForumReply.modifier'
        db.alter_column('forum_forumreply', 'modifier_id', self.gf('models.ForeignKey')(orm['auth.User'], null=True, editable=False))

        # Changing field 'ForumReply.subject'
        db.alter_column('forum_forumreply', 'subject', self.gf('models.CharField')(_('subject'), max_length=255))

        # Changing field 'ForumThread.status'
        db.alter_column('forum_forumthread', 'status', self.gf('models.IntegerField')(_("status")))

        # Changing field 'ForumThread.modified_date'
        db.alter_column('forum_forumthread', 'modified_date', self.gf('models.DateTimeField')(_("modified date"), null=True, editable=False))

        # Changing field 'ForumThread.forum'
        db.alter_column('forum_forumthread', 'forum_id', self.gf('models.ForeignKey')(orm['forum.Forum']))

        # Changing field 'ForumThread.is_sticky'
        db.alter_column('forum_forumthread', 'is_sticky', self.gf('models.BooleanField')(_("is sticky")))

        # Changing field 'ForumThread.views'
        db.alter_column('forum_forumthread', 'views', self.gf('models.IntegerField')(_("views"), editable=False))

        # Changing field 'ForumThread.creation_date'
        db.alter_column('forum_forumthread', 'creation_date', self.gf('models.DateTimeField')(_("creation date"), editable=False))

        # Changing field 'ForumThread.message'
        db.alter_column('forum_forumthread', 'message', self.gf('ExtendedTextField')(_('message')))

        # Changing field 'ForumThread.modifier'
        db.alter_column('forum_forumthread', 'modifier_id', self.gf('models.ForeignKey')(orm['auth.User'], null=True, editable=False))

        # Changing field 'ForumThread.creator'
        db.alter_column('forum_forumthread', 'creator_id', self.gf('models.ForeignKey')(orm['auth.User'], null=True, editable=False))

        # Changing field 'ForumThread.subject'
        db.alter_column('forum_forumthread', 'subject', self.gf('models.CharField')(_('subject'), max_length=255))
    
    
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'ordering': "('username',)", 'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('app_label', 'name')", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'forum.forum': {
            'Meta': {'ordering': "['tree_id', 'lft']", 'object_name': 'Forum'},
            'container': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.ForumContainer']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'forum_creator'", 'null': 'True', 'to': "orm['auth.User']"}),
            'description': ('base_libs.models.fields.ExtendedTextField', [], {'blank': 'True'}),
            'description_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'forum_modifier'", 'null': 'True', 'to': "orm['auth.User']"}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'child_set'", 'null': 'True', 'to': "orm['forum.Forum']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'forum.forumcontainer': {
            'Meta': {'ordering': "('title',)", 'object_name': 'ForumContainer'},
            'allow_bumping': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_level': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'object_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['sites.Site']", 'null': 'True', 'blank': 'True'}),
            'sysname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        'forum.forumreply': {
            'Meta': {'ordering': "['tree_id', 'lft']", 'object_name': 'ForumReply'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'forumreply_creator'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'message': ('base_libs.models.fields.ExtendedTextField', [], {}),
            'message_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'forumreply_modifier'", 'null': 'True', 'to': "orm['auth.User']"}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'child_set'", 'null': 'True', 'to': "orm['forum.ForumReply']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.ForumThread']"}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'forum.forumthread': {
            'Meta': {'ordering': "['forum', '-is_sticky', 'creation_date']", 'object_name': 'ForumThread'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'forumthread_creator'", 'null': 'True', 'to': "orm['auth.User']"}),
            'forum': ('mptt.fields.TreeForeignKey', [], {'to': "orm['forum.Forum']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_sticky': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'message': ('base_libs.models.fields.ExtendedTextField', [], {}),
            'message_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'forumthread_modifier'", 'null': 'True', 'to': "orm['auth.User']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'permissions.rowlevelpermission': {
            'Meta': {'object_name': 'RowLevelPermission', 'db_table': "'auth_rowlevelpermission'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'negative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'owner_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owner'", 'to': "orm['contenttypes.ContentType']"}),
            'owner_object_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.Permission']"})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['forum']
