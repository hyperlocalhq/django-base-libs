# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Deleting field 'individualrelationtype.path'
        db.delete_column('individual_relations_individualrelationtype', 'path')

        # Adding field 'IndividualRelationType.lft'
        db.add_column('individual_relations_individualrelationtype', 'lft', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True), keep_default=False)

        # Adding field 'IndividualRelationType.rght'
        db.add_column('individual_relations_individualrelationtype', 'rght', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True), keep_default=False)

        # Adding field 'IndividualRelationType.tree_id'
        db.add_column('individual_relations_individualrelationtype', 'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True), keep_default=False)

        # Adding field 'IndividualRelationType.level'
        db.add_column('individual_relations_individualrelationtype', 'level', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True), keep_default=False)

        # Changing field 'IndividualRelationType.backwards'
        db.alter_column('individual_relations_individualrelationtype', 'backwards_id', self.gf('mptt.fields.TreeForeignKey')(null=True, to=orm['individual_relations.IndividualRelationType']))

        # Changing field 'IndividualRelationType.parent'
        db.alter_column('individual_relations_individualrelationtype', 'parent_id', self.gf('mptt.fields.TreeForeignKey')(null=True, to=orm['individual_relations.IndividualRelationType']))

        # Changing field 'IndividualRelationType.title'
        db.alter_column('individual_relations_individualrelationtype', 'title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True))

        # Changing field 'IndividualRelationType.sort_order'
        db.alter_column('individual_relations_individualrelationtype', 'sort_order', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'IndividualRelation.status'
        db.alter_column('individual_relations_individualrelation', 'status', self.gf('django.db.models.fields.CharField')(max_length=10))

        # Changing field 'IndividualRelation.display_address'
        db.alter_column('individual_relations_individualrelation', 'display_address', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'IndividualRelation.display_birthday'
        db.alter_column('individual_relations_individualrelation', 'display_birthday', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'IndividualRelation.timestamp'
        db.alter_column('individual_relations_individualrelation', 'timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'IndividualRelation.activation'
        db.alter_column('individual_relations_individualrelation', 'activation', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'IndividualRelation.to_user'
        db.alter_column('individual_relations_individualrelation', 'to_user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'IndividualRelation.user'
        db.alter_column('individual_relations_individualrelation', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'IndividualRelation.display_phone'
        db.alter_column('individual_relations_individualrelation', 'display_phone', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'IndividualRelation.display_im'
        db.alter_column('individual_relations_individualrelation', 'display_im', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'IndividualRelation.message'
        db.alter_column('individual_relations_individualrelation', 'message', self.gf('django.db.models.fields.TextField')())

        # Changing field 'IndividualRelation.display_mobile'
        db.alter_column('individual_relations_individualrelation', 'display_mobile', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'IndividualRelation.display_fax'
        db.alter_column('individual_relations_individualrelation', 'display_fax', self.gf('django.db.models.fields.BooleanField')())
    
    
    def backwards(self, orm):
        
        # Adding field 'individualrelationtype.path'
        db.add_column('individual_relations_individualrelationtype', 'path', self.gf('models.CharField')(_('path'), null=True, max_length=8192, editable=False), keep_default=False)

        # Deleting field 'IndividualRelationType.lft'
        db.delete_column('individual_relations_individualrelationtype', 'lft')

        # Deleting field 'IndividualRelationType.rght'
        db.delete_column('individual_relations_individualrelationtype', 'rght')

        # Deleting field 'IndividualRelationType.tree_id'
        db.delete_column('individual_relations_individualrelationtype', 'tree_id')

        # Deleting field 'IndividualRelationType.level'
        db.delete_column('individual_relations_individualrelationtype', 'level')

        # Changing field 'IndividualRelationType.backwards'
        db.alter_column('individual_relations_individualrelationtype', 'backwards_id', self.gf('models.ForeignKey')(orm['individual_relations.IndividualRelationType'], null=True))

        # Changing field 'IndividualRelationType.parent'
        db.alter_column('individual_relations_individualrelationtype', 'parent_id', self.gf('models.ForeignKey')(orm['individual_relations.IndividualRelationType'], null=True))

        # Changing field 'IndividualRelationType.title'
        db.alter_column('individual_relations_individualrelationtype', 'title', self.gf('MultilingualCharField')(_('title'), max_length=255))

        # Changing field 'IndividualRelationType.sort_order'
        db.alter_column('individual_relations_individualrelationtype', 'sort_order', self.gf('models.IntegerField')(_("sort order"), editable=False))

        # Changing field 'IndividualRelation.status'
        db.alter_column('individual_relations_individualrelation', 'status', self.gf('models.CharField')(_("Status of the user #1"), max_length=10))

        # Changing field 'IndividualRelation.display_address'
        db.alter_column('individual_relations_individualrelation', 'display_address', self.gf('models.BooleanField')(_("Display address data to user #2")))

        # Changing field 'IndividualRelation.display_birthday'
        db.alter_column('individual_relations_individualrelation', 'display_birthday', self.gf('models.BooleanField')(_("Display birthday to user #2")))

        # Changing field 'IndividualRelation.timestamp'
        db.alter_column('individual_relations_individualrelation', 'timestamp', self.gf('models.DateTimeField')(_("Created"), auto_now_add=True, null=True, editable=False))

        # Changing field 'IndividualRelation.activation'
        db.alter_column('individual_relations_individualrelation', 'activation', self.gf('models.DateTimeField')(_("Activated"), null=True, editable=False))

        # Changing field 'IndividualRelation.to_user'
        db.alter_column('individual_relations_individualrelation', 'to_user_id', self.gf('models.ForeignKey')(orm['auth.User']))

        # Changing field 'IndividualRelation.user'
        db.alter_column('individual_relations_individualrelation', 'user_id', self.gf('models.ForeignKey')(orm['auth.User']))

        # Changing field 'IndividualRelation.display_phone'
        db.alter_column('individual_relations_individualrelation', 'display_phone', self.gf('models.BooleanField')(_("Display phone numbers to user #2")))

        # Changing field 'IndividualRelation.display_im'
        db.alter_column('individual_relations_individualrelation', 'display_im', self.gf('models.BooleanField')(_("Display instant messengers to user #2")))

        # Changing field 'IndividualRelation.message'
        db.alter_column('individual_relations_individualrelation', 'message', self.gf('models.TextField')(_("Message from user #1 to user #2")))

        # Changing field 'IndividualRelation.display_mobile'
        db.alter_column('individual_relations_individualrelation', 'display_mobile', self.gf('models.BooleanField')(_("Display mobile phones to user #2")))

        # Changing field 'IndividualRelation.display_fax'
        db.alter_column('individual_relations_individualrelation', 'display_fax', self.gf('models.BooleanField')(_("Display fax numbers to user #2")))
    
    
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
        'individual_relations.individualrelation': {
            'Meta': {'unique_together': "(('user', 'to_user'),)", 'object_name': 'IndividualRelation'},
            'activation': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'display_address': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'display_birthday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'display_fax': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'display_im': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'display_mobile': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'display_phone': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'relation_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['individual_relations.IndividualRelationType']", 'symmetrical': 'False', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'to_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_user'", 'to': "orm['auth.User']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'individual_relations.individualrelationtype': {
            'Meta': {'ordering': "['tree_id', 'lft']", 'object_name': 'IndividualRelationType'},
            'backwards': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'backwards_relation_set'", 'null': 'True', 'to': "orm['individual_relations.IndividualRelationType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'child_set'", 'null': 'True', 'to': "orm['individual_relations.IndividualRelationType']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
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
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['individual_relations']
