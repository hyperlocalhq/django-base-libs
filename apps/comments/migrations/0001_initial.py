# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from jetson.apps.comments.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'UserRating'
        db.create_table('comments_userrating', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('user', models.ForeignKey(orm['auth.User'])),
            ('comment', models.ForeignKey(orm.Comment)),
            ('rate_date', models.DateTimeField(_('rate date'), auto_now_add=True)),
            ('rate_index', models.SmallIntegerField(_('rate index'))),
        )))
        db.send_create_signal('comments', ['UserRating'])
        
        # Adding model 'ModeratorDeletionReason'
        db.create_table('comments_moderatordeletionreason', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('title', MultilingualCharField(_('title'), max_length=255)),
            ('reason', MultilingualTextField(_('reason'))),
            ('title_de', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('title_en', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('reason_de', ExtendedTextField(u'reason', unique_for_month=None, unique=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=False, null=False, unique_for_date=None, db_tablespace='', db_index=False)),
            ('reason_de_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('reason_en', ExtendedTextField(u'reason', unique_for_month=None, unique=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=False, null=False, unique_for_date=None, db_tablespace='', db_index=False)),
            ('reason_en_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('reason_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
        )))
        db.send_create_signal('comments', ['ModeratorDeletionReason'])
        
        # Adding model 'KarmaScore'
        db.create_table('comments_karmascore', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('user', models.ForeignKey(orm['auth.User'])),
            ('comment', models.ForeignKey(orm.Comment)),
            ('score', models.SmallIntegerField(_('score'), db_index=True)),
            ('scored_date', models.DateTimeField(_('score date'), auto_now=True)),
        )))
        db.send_create_signal('comments', ['KarmaScore'])
        
        # Adding model 'Comment'
        db.create_table('comments_comment', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('content_type', models.ForeignKey(orm['contenttypes.ContentType'], related_name=None, null=False, blank=False)),
            ('object_id', models.CharField(u'Related object', max_length=255, null=False, blank=False)),
            ('user', models.ForeignKey(orm['auth.User'], null=True, blank=True)),
            ('name', models.CharField(_('name'), max_length=80)),
            ('email', models.EmailField(_('email'), null=True, blank=True)),
            ('url_link', URLField(_("URL"), null=True, blank=True)),
            ('headline', models.CharField(_('headline'), max_length=255, null=True, blank=True)),
            ('comment', models.TextField(_('comment'), max_length=3000)),
            ('rating1', models.PositiveSmallIntegerField(_('rating #1'), null=True, blank=True)),
            ('rating2', models.PositiveSmallIntegerField(_('rating #2'), null=True, blank=True)),
            ('rating3', models.PositiveSmallIntegerField(_('rating #3'), null=True, blank=True)),
            ('rating4', models.PositiveSmallIntegerField(_('rating #4'), null=True, blank=True)),
            ('rating5', models.PositiveSmallIntegerField(_('rating #5'), null=True, blank=True)),
            ('rating6', models.PositiveSmallIntegerField(_('rating #6'), null=True, blank=True)),
            ('rating7', models.PositiveSmallIntegerField(_('rating #7'), null=True, blank=True)),
            ('rating8', models.PositiveSmallIntegerField(_('rating #8'), null=True, blank=True)),
            ('valid_rating', models.BooleanField(_('is valid rating'))),
            ('submit_date', models.DateTimeField(_('date/time submitted'), auto_now_add=True)),
            ('is_public', models.BooleanField(_('is public'))),
            ('ip_address', models.IPAddressField(_('IP address'), null=True, blank=True)),
            ('is_removed', models.BooleanField(_('is removed'), default=False)),
            ('is_spam', models.BooleanField(_('is_spam'), default=False)),
            ('site', models.ForeignKey(orm['sites.Site'])),
        )))
        db.send_create_signal('comments', ['Comment'])
        
        # Adding model 'UserFlag'
        db.create_table('comments_userflag', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('user', models.ForeignKey(orm['auth.User'])),
            ('comment', models.ForeignKey(orm.Comment)),
            ('flag_date', models.DateTimeField(_('flag date'), auto_now_add=True)),
        )))
        db.send_create_signal('comments', ['UserFlag'])
        
        # Adding model 'ModeratorDeletion'
        db.create_table('comments_moderatordeletion', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('user', models.ForeignKey(orm['auth.User'])),
            ('comment', models.ForeignKey(orm.Comment)),
            ('deletion_date', models.DateTimeField(_('deletion date'), auto_now_add=True)),
            ('deletion_reason', models.ForeignKey(orm.ModeratorDeletionReason)),
        )))
        db.send_create_signal('comments', ['ModeratorDeletion'])
        
        # Creating unique_together for [user, comment] on ModeratorDeletion.
        db.create_unique('comments_moderatordeletion', ['user_id', 'comment_id'])
        
        # Creating unique_together for [user, comment] on UserFlag.
        db.create_unique('comments_userflag', ['user_id', 'comment_id'])
        
        # Creating unique_together for [user, comment] on KarmaScore.
        db.create_unique('comments_karmascore', ['user_id', 'comment_id'])
        
        # Creating unique_together for [user, comment, rate_index] on UserRating.
        db.create_unique('comments_userrating', ['user_id', 'comment_id', 'rate_index'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'UserRating'
        db.delete_table('comments_userrating')
        
        # Deleting model 'ModeratorDeletionReason'
        db.delete_table('comments_moderatordeletionreason')
        
        # Deleting model 'KarmaScore'
        db.delete_table('comments_karmascore')
        
        # Deleting model 'Comment'
        db.delete_table('comments_comment')
        
        # Deleting model 'UserFlag'
        db.delete_table('comments_userflag')
        
        # Deleting model 'ModeratorDeletion'
        db.delete_table('comments_moderatordeletion')
        
        # Deleting unique_together for [user, comment] on ModeratorDeletion.
        db.delete_unique('comments_moderatordeletion', ['user_id', 'comment_id'])
        
        # Deleting unique_together for [user, comment] on UserFlag.
        db.delete_unique('comments_userflag', ['user_id', 'comment_id'])
        
        # Deleting unique_together for [user, comment] on KarmaScore.
        db.delete_unique('comments_karmascore', ['user_id', 'comment_id'])
        
        # Deleting unique_together for [user, comment, rate_index] on UserRating.
        db.delete_unique('comments_userrating', ['user_id', 'comment_id', 'rate_index'])
        
    
    
    models = {
        'comments.userrating': {
            'Meta': {'unique_together': "(('user','comment','rate_index'),)"},
            'comment': ('models.ForeignKey', ["orm['comments.Comment']"], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'rate_date': ('models.DateTimeField', ["_('rate date')"], {'auto_now_add': 'True'}),
            'rate_index': ('models.SmallIntegerField', ["_('rate index')"], {}),
            'user': ('models.ForeignKey', ["orm['auth.User']"], {})
        },
        'comments.moderatordeletionreason': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'reason': ('MultilingualTextField', ["_('reason')"], {}),
            'reason_de': ('ExtendedTextField', ["u'reason'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'False', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'reason_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'reason_en': ('ExtendedTextField', ["u'reason'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'False', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'reason_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'reason_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'title': ('MultilingualCharField', ["_('title')"], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'comments.karmascore': {
            'Meta': {'unique_together': "(('user','comment'),)"},
            'comment': ('models.ForeignKey', ["orm['comments.Comment']"], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'score': ('models.SmallIntegerField', ["_('score')"], {'db_index': 'True'}),
            'scored_date': ('models.DateTimeField', ["_('score date')"], {'auto_now': 'True'}),
            'user': ('models.ForeignKey', ["orm['auth.User']"], {})
        },
        'comments.comment': {
            'Meta': {'ordering': "('-submit_date',)"},
            'comment': ('models.TextField', ["_('comment')"], {'max_length': '3000'}),
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'related_name': 'None', 'null': 'False', 'blank': 'False'}),
            'email': ('models.EmailField', ["_('email')"], {'null': 'True', 'blank': 'True'}),
            'headline': ('models.CharField', ["_('headline')"], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('models.IPAddressField', ["_('IP address')"], {'null': 'True', 'blank': 'True'}),
            'is_public': ('models.BooleanField', ["_('is public')"], {}),
            'is_removed': ('models.BooleanField', ["_('is removed')"], {'default': 'False'}),
            'is_spam': ('models.BooleanField', ["_('is_spam')"], {'default': 'False'}),
            'name': ('models.CharField', ["_('name')"], {'max_length': '80'}),
            'object_id': ('models.CharField', ["u'Related object'"], {'max_length': '255', 'null': 'False', 'blank': 'False'}),
            'rating1': ('models.PositiveSmallIntegerField', ["_('rating #1')"], {'null': 'True', 'blank': 'True'}),
            'rating2': ('models.PositiveSmallIntegerField', ["_('rating #2')"], {'null': 'True', 'blank': 'True'}),
            'rating3': ('models.PositiveSmallIntegerField', ["_('rating #3')"], {'null': 'True', 'blank': 'True'}),
            'rating4': ('models.PositiveSmallIntegerField', ["_('rating #4')"], {'null': 'True', 'blank': 'True'}),
            'rating5': ('models.PositiveSmallIntegerField', ["_('rating #5')"], {'null': 'True', 'blank': 'True'}),
            'rating6': ('models.PositiveSmallIntegerField', ["_('rating #6')"], {'null': 'True', 'blank': 'True'}),
            'rating7': ('models.PositiveSmallIntegerField', ["_('rating #7')"], {'null': 'True', 'blank': 'True'}),
            'rating8': ('models.PositiveSmallIntegerField', ["_('rating #8')"], {'null': 'True', 'blank': 'True'}),
            'site': ('models.ForeignKey', ["orm['sites.Site']"], {}),
            'submit_date': ('models.DateTimeField', ["_('date/time submitted')"], {'auto_now_add': 'True'}),
            'url_link': ('URLField', ['_("URL")'], {'null': 'True', 'blank': 'True'}),
            'user': ('models.ForeignKey', ["orm['auth.User']"], {'null': 'True', 'blank': 'True'}),
            'valid_rating': ('models.BooleanField', ["_('is valid rating')"], {})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'db_table': "'django_site'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'comments.userflag': {
            'Meta': {'unique_together': "(('user','comment'),)"},
            'comment': ('models.ForeignKey', ["orm['comments.Comment']"], {}),
            'flag_date': ('models.DateTimeField', ["_('flag date')"], {'auto_now_add': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'user': ('models.ForeignKey', ["orm['auth.User']"], {})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'comments.moderatordeletion': {
            'Meta': {'unique_together': "(('user','comment'),)"},
            'comment': ('models.ForeignKey', ["orm['comments.Comment']"], {}),
            'deletion_date': ('models.DateTimeField', ["_('deletion date')"], {'auto_now_add': 'True'}),
            'deletion_reason': ('models.ForeignKey', ["orm['comments.ModeratorDeletionReason']"], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'user': ('models.ForeignKey', ["orm['auth.User']"], {})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['comments']
