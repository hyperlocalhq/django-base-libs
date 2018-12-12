# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Comment'
        db.create_table('comments_comment', south_cleaned_fields((
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('url_link', self.gf('base_libs.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('headline', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(max_length=3000)),
            ('rating1', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('rating2', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('rating3', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('rating4', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('rating5', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('rating6', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('rating7', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('rating8', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('valid_rating', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('submit_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
            ('is_removed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_spam', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
        )))
        db.send_create_signal('comments', ['Comment'])

        # Adding model 'KarmaScore'
        db.create_table('comments_karmascore', south_cleaned_fields((
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('comment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['comments.Comment'])),
            ('score', self.gf('django.db.models.fields.SmallIntegerField')(db_index=True)),
            ('scored_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        )))
        db.send_create_signal('comments', ['KarmaScore'])

        # Adding unique constraint on 'KarmaScore', fields ['user', 'comment']
        db.create_unique('comments_karmascore', ['user_id', 'comment_id'])

        # Adding model 'UserFlag'
        db.create_table('comments_userflag', south_cleaned_fields((
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('comment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['comments.Comment'])),
            ('flag_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        )))
        db.send_create_signal('comments', ['UserFlag'])

        # Adding unique constraint on 'UserFlag', fields ['user', 'comment']
        db.create_unique('comments_userflag', ['user_id', 'comment_id'])

        # Adding model 'ModeratorDeletionReason'
        db.create_table('comments_moderatordeletionreason', south_cleaned_fields((
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True)),
            ('reason', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True)),
            ('title_de', self.gf('django.db.models.fields.CharField')(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('title_en', self.gf('django.db.models.fields.CharField')(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('reason_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'reason', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=False, unique=False, db_tablespace='', db_index=False)),
            ('reason_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('reason_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'reason', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=False, unique=False, db_tablespace='', db_index=False)),
            ('reason_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('reason_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
        )))
        db.send_create_signal('comments', ['ModeratorDeletionReason'])

        # Adding model 'ModeratorDeletion'
        db.create_table('comments_moderatordeletion', south_cleaned_fields((
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('comment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['comments.Comment'])),
            ('deletion_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('deletion_reason', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['comments.ModeratorDeletionReason'])),
        )))
        db.send_create_signal('comments', ['ModeratorDeletion'])

        # Adding unique constraint on 'ModeratorDeletion', fields ['user', 'comment']
        db.create_unique('comments_moderatordeletion', ['user_id', 'comment_id'])

        # Adding model 'UserRating'
        db.create_table('comments_userrating', south_cleaned_fields((
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('comment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['comments.Comment'])),
            ('rate_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('rate_index', self.gf('django.db.models.fields.SmallIntegerField')()),
        )))
        db.send_create_signal('comments', ['UserRating'])

        # Adding unique constraint on 'UserRating', fields ['user', 'comment', 'rate_index']
        db.create_unique('comments_userrating', ['user_id', 'comment_id', 'rate_index'])
    
    
    def backwards(self, orm):
        
        # Removing unique constraint on 'UserRating', fields ['user', 'comment', 'rate_index']
        db.delete_unique('comments_userrating', ['user_id', 'comment_id', 'rate_index'])

        # Removing unique constraint on 'ModeratorDeletion', fields ['user', 'comment']
        db.delete_unique('comments_moderatordeletion', ['user_id', 'comment_id'])

        # Removing unique constraint on 'UserFlag', fields ['user', 'comment']
        db.delete_unique('comments_userflag', ['user_id', 'comment_id'])

        # Removing unique constraint on 'KarmaScore', fields ['user', 'comment']
        db.delete_unique('comments_karmascore', ['user_id', 'comment_id'])

        # Deleting model 'Comment'
        db.delete_table('comments_comment')

        # Deleting model 'KarmaScore'
        db.delete_table('comments_karmascore')

        # Deleting model 'UserFlag'
        db.delete_table('comments_userflag')

        # Deleting model 'ModeratorDeletionReason'
        db.delete_table('comments_moderatordeletionreason')

        # Deleting model 'ModeratorDeletion'
        db.delete_table('comments_moderatordeletion')

        # Deleting model 'UserRating'
        db.delete_table('comments_userrating')
    
    
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
        'comments.comment': {
            'Meta': {'ordering': "('-submit_date',)", 'object_name': 'Comment'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '3000'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_spam': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'object_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'rating1': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rating2': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rating3': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rating4': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rating5': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rating6': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rating7': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rating8': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'submit_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'url_link': ('base_libs.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'valid_rating': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'comments.karmascore': {
            'Meta': {'unique_together': "(('user', 'comment'),)", 'object_name': 'KarmaScore'},
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['comments.Comment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.SmallIntegerField', [], {'db_index': 'True'}),
            'scored_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'comments.moderatordeletion': {
            'Meta': {'unique_together': "(('user', 'comment'),)", 'object_name': 'ModeratorDeletion'},
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['comments.Comment']"}),
            'deletion_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deletion_reason': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['comments.ModeratorDeletionReason']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'comments.moderatordeletionreason': {
            'Meta': {'object_name': 'ModeratorDeletionReason'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True'}),
            'reason_de': ('base_libs.models.fields.ExtendedTextField', ["u'reason'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'False', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'reason_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'reason_en': ('base_libs.models.fields.ExtendedTextField', ["u'reason'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'False', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'reason_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'reason_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'comments.userflag': {
            'Meta': {'unique_together': "(('user', 'comment'),)", 'object_name': 'UserFlag'},
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['comments.Comment']"}),
            'flag_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'comments.userrating': {
            'Meta': {'unique_together': "(('user', 'comment', 'rate_index'),)", 'object_name': 'UserRating'},
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['comments.Comment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rate_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'rate_index': ('django.db.models.fields.SmallIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('app_label', 'name')", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
    
    complete_apps = ['comments']
