# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
                # Adding field 'InfoBlock.title_fr'
        db.add_column(u'blocks_infoblock', 'title_fr',
                      self.gf('django.db.models.fields.CharField')(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=512, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'InfoBlock.title_pl'
        db.add_column(u'blocks_infoblock', 'title_pl',
                      self.gf('django.db.models.fields.CharField')(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=512, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'InfoBlock.title_tr'
        db.add_column(u'blocks_infoblock', 'title_tr',
                      self.gf('django.db.models.fields.CharField')(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=512, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'InfoBlock.title_es'
        db.add_column(u'blocks_infoblock', 'title_es',
                      self.gf('django.db.models.fields.CharField')(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=512, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'InfoBlock.title_it'
        db.add_column(u'blocks_infoblock', 'title_it',
                      self.gf('django.db.models.fields.CharField')(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=512, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'InfoBlock.content_fr'
        db.add_column(u'blocks_infoblock', 'content_fr',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'content', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'InfoBlock.content_fr_markup_type'
        db.add_column(u'blocks_infoblock', 'content_fr_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'InfoBlock.content_pl'
        db.add_column(u'blocks_infoblock', 'content_pl',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'content', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'InfoBlock.content_pl_markup_type'
        db.add_column(u'blocks_infoblock', 'content_pl_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'InfoBlock.content_tr'
        db.add_column(u'blocks_infoblock', 'content_tr',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'content', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'InfoBlock.content_tr_markup_type'
        db.add_column(u'blocks_infoblock', 'content_tr_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'InfoBlock.content_es'
        db.add_column(u'blocks_infoblock', 'content_es',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'content', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'InfoBlock.content_es_markup_type'
        db.add_column(u'blocks_infoblock', 'content_es_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'InfoBlock.content_it'
        db.add_column(u'blocks_infoblock', 'content_it',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'content', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'InfoBlock.content_it_markup_type'
        db.add_column(u'blocks_infoblock', 'content_it_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

    
    
    def backwards(self, orm):
                # Deleting field 'InfoBlock.title_fr'
        db.delete_column(u'blocks_infoblock', 'title_fr')

        # Deleting field 'InfoBlock.title_pl'
        db.delete_column(u'blocks_infoblock', 'title_pl')

        # Deleting field 'InfoBlock.title_tr'
        db.delete_column(u'blocks_infoblock', 'title_tr')

        # Deleting field 'InfoBlock.title_es'
        db.delete_column(u'blocks_infoblock', 'title_es')

        # Deleting field 'InfoBlock.title_it'
        db.delete_column(u'blocks_infoblock', 'title_it')

        # Deleting field 'InfoBlock.content_fr'
        db.delete_column(u'blocks_infoblock', 'content_fr')

        # Deleting field 'InfoBlock.content_fr_markup_type'
        db.delete_column(u'blocks_infoblock', 'content_fr_markup_type')

        # Deleting field 'InfoBlock.content_pl'
        db.delete_column(u'blocks_infoblock', 'content_pl')

        # Deleting field 'InfoBlock.content_pl_markup_type'
        db.delete_column(u'blocks_infoblock', 'content_pl_markup_type')

        # Deleting field 'InfoBlock.content_tr'
        db.delete_column(u'blocks_infoblock', 'content_tr')

        # Deleting field 'InfoBlock.content_tr_markup_type'
        db.delete_column(u'blocks_infoblock', 'content_tr_markup_type')

        # Deleting field 'InfoBlock.content_es'
        db.delete_column(u'blocks_infoblock', 'content_es')

        # Deleting field 'InfoBlock.content_es_markup_type'
        db.delete_column(u'blocks_infoblock', 'content_es_markup_type')

        # Deleting field 'InfoBlock.content_it'
        db.delete_column(u'blocks_infoblock', 'content_it')

        # Deleting field 'InfoBlock.content_it_markup_type'
        db.delete_column(u'blocks_infoblock', 'content_it_markup_type')

    
    
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
        u'blocks.infoblock': {
            'Meta': {'ordering': "['sysname']", 'object_name': 'InfoBlock'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'infoblock_author'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'content': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True'}),
            'content_de': ('base_libs.models.fields.ExtendedTextField', ["u'content'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'content_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'content_en': ('base_libs.models.fields.ExtendedTextField', ["u'content'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'content_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'content_es': ('base_libs.models.fields.ExtendedTextField', ["u'content'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'content_es_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'content_fr': ('base_libs.models.fields.ExtendedTextField', ["u'content'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'content_fr_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'content_it': ('base_libs.models.fields.ExtendedTextField', ["u'content'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'content_it_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'content_pl': ('base_libs.models.fields.ExtendedTextField', ["u'content'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'content_pl_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'content_tr': ('base_libs.models.fields.ExtendedTextField', ["u'content'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'content_tr_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published_from': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'published_till': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'sysname': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '512', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '512', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_es': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '512', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_fr': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '512', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_it': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '512', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_pl': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '512', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_tr': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '512', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
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
    
    complete_apps = ['blocks']
