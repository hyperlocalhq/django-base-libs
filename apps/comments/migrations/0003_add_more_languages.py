# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
                # Deleting field 'ModeratorDeletionReason.reason_markup_type'
        db.delete_column(u'comments_moderatordeletionreason', 'reason_markup_type')

        # Adding field 'ModeratorDeletionReason.title_fr'
        db.add_column(u'comments_moderatordeletionreason', 'title_fr',
                      self.gf('django.db.models.fields.CharField')(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'ModeratorDeletionReason.title_pl'
        db.add_column(u'comments_moderatordeletionreason', 'title_pl',
                      self.gf('django.db.models.fields.CharField')(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'ModeratorDeletionReason.title_tr'
        db.add_column(u'comments_moderatordeletionreason', 'title_tr',
                      self.gf('django.db.models.fields.CharField')(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'ModeratorDeletionReason.title_es'
        db.add_column(u'comments_moderatordeletionreason', 'title_es',
                      self.gf('django.db.models.fields.CharField')(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'ModeratorDeletionReason.title_it'
        db.add_column(u'comments_moderatordeletionreason', 'title_it',
                      self.gf('django.db.models.fields.CharField')(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'ModeratorDeletionReason.reason_fr'
        db.add_column(u'comments_moderatordeletionreason', 'reason_fr',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'reason', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'ModeratorDeletionReason.reason_fr_markup_type'
        db.add_column(u'comments_moderatordeletionreason', 'reason_fr_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'ModeratorDeletionReason.reason_pl'
        db.add_column(u'comments_moderatordeletionreason', 'reason_pl',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'reason', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'ModeratorDeletionReason.reason_pl_markup_type'
        db.add_column(u'comments_moderatordeletionreason', 'reason_pl_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'ModeratorDeletionReason.reason_tr'
        db.add_column(u'comments_moderatordeletionreason', 'reason_tr',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'reason', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'ModeratorDeletionReason.reason_tr_markup_type'
        db.add_column(u'comments_moderatordeletionreason', 'reason_tr_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'ModeratorDeletionReason.reason_es'
        db.add_column(u'comments_moderatordeletionreason', 'reason_es',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'reason', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'ModeratorDeletionReason.reason_es_markup_type'
        db.add_column(u'comments_moderatordeletionreason', 'reason_es_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'ModeratorDeletionReason.reason_it'
        db.add_column(u'comments_moderatordeletionreason', 'reason_it',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'reason', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'ModeratorDeletionReason.reason_it_markup_type'
        db.add_column(u'comments_moderatordeletionreason', 'reason_it_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)


    def backwards(self, orm):
                # Adding field 'ModeratorDeletionReason.reason_markup_type'
        db.add_column(u'comments_moderatordeletionreason', 'reason_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Deleting field 'ModeratorDeletionReason.title_fr'
        db.delete_column(u'comments_moderatordeletionreason', 'title_fr')

        # Deleting field 'ModeratorDeletionReason.title_pl'
        db.delete_column(u'comments_moderatordeletionreason', 'title_pl')

        # Deleting field 'ModeratorDeletionReason.title_tr'
        db.delete_column(u'comments_moderatordeletionreason', 'title_tr')

        # Deleting field 'ModeratorDeletionReason.title_es'
        db.delete_column(u'comments_moderatordeletionreason', 'title_es')

        # Deleting field 'ModeratorDeletionReason.title_it'
        db.delete_column(u'comments_moderatordeletionreason', 'title_it')

        # Deleting field 'ModeratorDeletionReason.reason_fr'
        db.delete_column(u'comments_moderatordeletionreason', 'reason_fr')

        # Deleting field 'ModeratorDeletionReason.reason_fr_markup_type'
        db.delete_column(u'comments_moderatordeletionreason', 'reason_fr_markup_type')

        # Deleting field 'ModeratorDeletionReason.reason_pl'
        db.delete_column(u'comments_moderatordeletionreason', 'reason_pl')

        # Deleting field 'ModeratorDeletionReason.reason_pl_markup_type'
        db.delete_column(u'comments_moderatordeletionreason', 'reason_pl_markup_type')

        # Deleting field 'ModeratorDeletionReason.reason_tr'
        db.delete_column(u'comments_moderatordeletionreason', 'reason_tr')

        # Deleting field 'ModeratorDeletionReason.reason_tr_markup_type'
        db.delete_column(u'comments_moderatordeletionreason', 'reason_tr_markup_type')

        # Deleting field 'ModeratorDeletionReason.reason_es'
        db.delete_column(u'comments_moderatordeletionreason', 'reason_es')

        # Deleting field 'ModeratorDeletionReason.reason_es_markup_type'
        db.delete_column(u'comments_moderatordeletionreason', 'reason_es_markup_type')

        # Deleting field 'ModeratorDeletionReason.reason_it'
        db.delete_column(u'comments_moderatordeletionreason', 'reason_it')

        # Deleting field 'ModeratorDeletionReason.reason_it_markup_type'
        db.delete_column(u'comments_moderatordeletionreason', 'reason_it_markup_type')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'ordering': "('username',)", 'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'comments.comment': {
            'Meta': {'ordering': "('-submit_date',)", 'object_name': 'Comment'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '3000'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'submit_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'url_link': ('base_libs.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'valid_rating': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'comments.karmascore': {
            'Meta': {'unique_together': "(('user', 'comment'),)", 'object_name': 'KarmaScore'},
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['comments.Comment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.SmallIntegerField', [], {'db_index': 'True'}),
            'scored_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'comments.moderatordeletion': {
            'Meta': {'unique_together': "(('user', 'comment'),)", 'object_name': 'ModeratorDeletion'},
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['comments.Comment']"}),
            'deletion_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deletion_reason': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['comments.ModeratorDeletionReason']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'comments.moderatordeletionreason': {
            'Meta': {'object_name': 'ModeratorDeletionReason'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True'}),
            'reason_de': ('base_libs.models.fields.ExtendedTextField', ["u'reason'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'reason_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'reason_en': ('base_libs.models.fields.ExtendedTextField', ["u'reason'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'reason_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'reason_es': ('base_libs.models.fields.ExtendedTextField', ["u'reason'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'reason_es_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'reason_fr': ('base_libs.models.fields.ExtendedTextField', ["u'reason'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'reason_fr_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'reason_it': ('base_libs.models.fields.ExtendedTextField', ["u'reason'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'reason_it_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'reason_pl': ('base_libs.models.fields.ExtendedTextField', ["u'reason'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'reason_pl_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'reason_tr': ('base_libs.models.fields.ExtendedTextField', ["u'reason'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'reason_tr_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_es': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_fr': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_it': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_pl': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_tr': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        u'comments.userflag': {
            'Meta': {'unique_together': "(('user', 'comment'),)", 'object_name': 'UserFlag'},
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['comments.Comment']"}),
            'flag_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'comments.userrating': {
            'Meta': {'unique_together': "(('user', 'comment', 'rate_index'),)", 'object_name': 'UserRating'},
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['comments.Comment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rate_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'rate_index': ('django.db.models.fields.SmallIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('app_label', 'name')", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'permissions.rowlevelpermission': {
            'Meta': {'object_name': 'RowLevelPermission', 'db_table': "'auth_rowlevelpermission'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'negative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'owner_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owner'", 'to': u"orm['contenttypes.ContentType']"}),
            'owner_object_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Permission']"})
        },
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['comments']
