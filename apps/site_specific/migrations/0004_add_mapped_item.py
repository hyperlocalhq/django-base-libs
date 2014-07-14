# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'MappedItem'
        db.create_table('site_specific_mappeditem', south_cleaned_fields((
            ('object_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('rendered_de', self.gf('django.db.models.fields.TextField')()),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('rendered_en', self.gf('django.db.models.fields.TextField')()),
            ('lng', self.gf('django.db.models.fields.FloatField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        )))
        db.send_create_signal('site_specific', ['MappedItem'])

        # Changing field 'ClaimRequest.phone_number'
        db.alter_column('system_claimrequest', 'phone_number', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True))

        # Changing field 'ClaimRequest.modified_date'
        db.alter_column('system_claimrequest', 'modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True))

        # Changing field 'ClaimRequest.phone_country'
        db.alter_column('system_claimrequest', 'phone_country', self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True))

        # Changing field 'ClaimRequest.best_time_to_call'
        db.alter_column('system_claimrequest', 'best_time_to_call', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True))

        # Changing field 'ClaimRequest.name'
        db.alter_column('system_claimrequest', 'name', self.gf('django.db.models.fields.CharField')(max_length=80))

        # Changing field 'ClaimRequest.comments'
        db.alter_column('system_claimrequest', 'comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True))

        # Changing field 'ClaimRequest.email'
        db.alter_column('system_claimrequest', 'email', self.gf('django.db.models.fields.EmailField')(max_length=75))

        # Changing field 'ClaimRequest.status'
        db.alter_column('system_claimrequest', 'status', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True))

        # Changing field 'ClaimRequest.user'
        db.alter_column('system_claimrequest', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'ClaimRequest.content_type'
        db.alter_column('system_claimrequest', 'content_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType']))

        # Changing field 'ClaimRequest.created_date'
        db.alter_column('system_claimrequest', 'created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True))

        # Changing field 'ClaimRequest.role'
        db.alter_column('system_claimrequest', 'role', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True))

        # Changing field 'ClaimRequest.phone_area'
        db.alter_column('system_claimrequest', 'phone_area', self.gf('django.db.models.fields.CharField')(max_length=5, null=True, blank=True))

        # Changing field 'ClaimRequest.modifier'
        db.alter_column('system_claimrequest', 'modifier_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['auth.User']))

        # Changing field 'ContextItem.status'
        db.alter_column('system_contextitem', 'status_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['structure.Term']))

        # Changing field 'ContextItem.location_type'
        db.alter_column('system_contextitem', 'location_type_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['structure.Term']))

        # Changing field 'ContextItem.description'
        db.alter_column('system_contextitem', 'description', self.gf('base_libs.models.fields.MultilingualTextField')(null=True, blank=True))

        # Changing field 'ContextItem.title'
        db.alter_column('system_contextitem', 'title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True, blank=True))

        # Changing field 'ContextItem.description_en'
        db.alter_column('system_contextitem', 'description_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace=''))

        # Changing field 'ContextItem.creation_date'
        db.alter_column('system_contextitem', 'creation_date', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'ContextItem.modified_date'
        db.alter_column('system_contextitem', 'modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'ContextItem.content_type'
        db.alter_column('system_contextitem', 'content_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType']))

        # Changing field 'ContextItem.description_de'
        db.alter_column('system_contextitem', 'description_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace=''))
    
    
    def backwards(self, orm):
        
        # Deleting model 'MappedItem'
        db.delete_table('site_specific_mappeditem')

        # Changing field 'ClaimRequest.phone_number'
        db.alter_column('system_claimrequest', 'phone_number', self.gf('django.db.models.fields.CharField')(_("Phone Number"), max_length=15, null=True, blank=True))

        # Changing field 'ClaimRequest.modified_date'
        db.alter_column('system_claimrequest', 'modified_date', self.gf('django.db.models.fields.DateTimeField')(_("Modified"), auto_now=True))

        # Changing field 'ClaimRequest.phone_country'
        db.alter_column('system_claimrequest', 'phone_country', self.gf('django.db.models.fields.CharField')(_("Country Code"), max_length=4, null=True, blank=True))

        # Changing field 'ClaimRequest.best_time_to_call'
        db.alter_column('system_claimrequest', 'best_time_to_call', self.gf('django.db.models.fields.CharField')(_("Best Time to Call"), max_length=25, null=True, blank=True))

        # Changing field 'ClaimRequest.name'
        db.alter_column('system_claimrequest', 'name', self.gf('django.db.models.fields.CharField')(_('Name'), max_length=80))

        # Changing field 'ClaimRequest.comments'
        db.alter_column('system_claimrequest', 'comments', self.gf('django.db.models.fields.TextField')(_('Comments'), null=True, blank=True))

        # Changing field 'ClaimRequest.email'
        db.alter_column('system_claimrequest', 'email', self.gf('django.db.models.fields.EmailField')(_('Email')))

        # Changing field 'ClaimRequest.status'
        db.alter_column('system_claimrequest', 'status', self.gf('django.db.models.fields.IntegerField')(_("Status"), null=True, blank=True))

        # Changing field 'ClaimRequest.user'
        db.alter_column('system_claimrequest', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(orm['auth.User']))

        # Changing field 'ClaimRequest.content_type'
        db.alter_column('system_claimrequest', 'content_type_id', self.gf('django.db.models.fields.related.ForeignKey')(orm['contenttypes.ContentType'], null=False, blank=False))

        # Changing field 'ClaimRequest.created_date'
        db.alter_column('system_claimrequest', 'created_date', self.gf('django.db.models.fields.DateTimeField')(_("Created"), auto_now_add=True))

        # Changing field 'ClaimRequest.role'
        db.alter_column('system_claimrequest', 'role', self.gf('django.db.models.fields.CharField')(_('Role'), max_length=80, null=True, blank=True))

        # Changing field 'ClaimRequest.phone_area'
        db.alter_column('system_claimrequest', 'phone_area', self.gf('django.db.models.fields.CharField')(_("Area Code"), max_length=5, null=True, blank=True))

        # Changing field 'ClaimRequest.modifier'
        db.alter_column('system_claimrequest', 'modifier_id', self.gf('django.db.models.fields.related.ForeignKey')(orm['auth.User'], null=True, blank=True))

        # Changing field 'ContextItem.status'
        db.alter_column('system_contextitem', 'status_id', self.gf('django.db.models.fields.related.ForeignKey')(orm['structure.Term'], limit_choices_to={'vocabulary__sysname':'basics_object_statuses'}, null=True, blank=True))

        # Changing field 'ContextItem.location_type'
        db.alter_column('system_contextitem', 'location_type_id', self.gf('django.db.models.fields.related.ForeignKey')(orm['structure.Term'], limit_choices_to={'vocabulary__sysname':'basics_locality'}, null=True, blank=True))

        # Changing field 'ContextItem.description'
        db.alter_column('system_contextitem', 'description', self.gf('base_libs.models.fields.MultilingualTextField')(_("Description"), blank=True))

        # Changing field 'ContextItem.title'
        db.alter_column('system_contextitem', 'title', self.gf('base_libs.models.fields.MultilingualCharField')(_("Title"), max_length=255, blank=True))

        # Changing field 'ContextItem.description_en'
        db.alter_column('system_contextitem', 'description_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, unique_for_date=None, db_tablespace=''))

        # Changing field 'ContextItem.creation_date'
        db.alter_column('system_contextitem', 'creation_date', self.gf('django.db.models.fields.DateTimeField')(_("creation date"), editable=False))

        # Changing field 'ContextItem.modified_date'
        db.alter_column('system_contextitem', 'modified_date', self.gf('django.db.models.fields.DateTimeField')(_("modified date"), null=True, editable=False))

        # Changing field 'ContextItem.content_type'
        db.alter_column('system_contextitem', 'content_type_id', self.gf('django.db.models.fields.related.ForeignKey')(orm['contenttypes.ContentType'], null=False, blank=False))

        # Changing field 'ContextItem.description_de'
        db.alter_column('system_contextitem', 'description_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, unique_for_date=None, db_tablespace=''))
    
    
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'permissions.rowlevelpermission': {
            'Meta': {'object_name': 'RowLevelPermission', 'db_table': "'auth_rowlevelpermission'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'negative': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owner'", 'to': "orm['contenttypes.ContentType']"}),
            'owner_object_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.Permission']"})
        },
        'site_specific.claimrequest': {
            'Meta': {'object_name': 'ClaimRequest', 'db_table': "'system_claimrequest'"},
            'best_time_to_call': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'claimrequest_modifier'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'object_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone_area': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'phone_country': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'claimrequest_user'", 'to': "orm['auth.User']"})
        },
        'site_specific.contextitem': {
            'Meta': {'object_name': 'ContextItem', 'db_table': "'system_contextitem'"},
            'additional_search_data': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'context_categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['structure.ContextCategory']", 'symmetrical': 'False', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creative_sectors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'creative_industry_contextitems'", 'blank': 'True', 'to': "orm['structure.Term']"}),
            'description': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'description_de': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'locality_contextitems'", 'blank': 'True', 'null': 'True', 'to': "orm['structure.Term']"}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'object_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'object_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'object_type_contextitems'", 'blank': 'True', 'to': "orm['structure.Term']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'db_index': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'status_contextitems'", 'blank': 'True', 'null': 'True', 'to': "orm['structure.Term']"}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        'site_specific.mappeditem': {
            'Meta': {'object_name': 'MappedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lng': ('django.db.models.fields.FloatField', [], {}),
            'object_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rendered_de': ('django.db.models.fields.TextField', [], {}),
            'rendered_en': ('django.db.models.fields.TextField', [], {})
        },
        'structure.contextcategory': {
            'Meta': {'object_name': 'ContextCategory'},
            'body': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'body_de': ('base_libs.models.fields.ExtendedTextField', ["u'body'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'body_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'body_en': ('base_libs.models.fields.ExtendedTextField', ["u'body'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'body_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'body_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'creative_sectors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['structure.Term']", 'symmetrical': 'False', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']", 'blank': 'True'}),
            'is_applied4document': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_applied4event': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_applied4institution': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_applied4person': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_applied4persongroup': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'child_set'", 'blank': 'True', 'null': 'True', 'to': "orm['structure.ContextCategory']"}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '8192', 'null': 'True'}),
            'path_search': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'sysname': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'db_index': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'structure.term': {
            'Meta': {'object_name': 'Term'},
            'body': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'body_de': ('base_libs.models.fields.ExtendedTextField', ["u'body'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'body_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'body_en': ('base_libs.models.fields.ExtendedTextField', ["u'body'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'body_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'body_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']", 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'child_set'", 'blank': 'True', 'null': 'True', 'to': "orm['structure.Term']"}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '8192', 'null': 'True'}),
            'path_search': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'sysname': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'db_index': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'vocabulary': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structure.Vocabulary']"})
        },
        'structure.vocabulary': {
            'Meta': {'object_name': 'Vocabulary'},
            'body': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'body_de': ('base_libs.models.fields.ExtendedTextField', ["u'body'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'body_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'body_en': ('base_libs.models.fields.ExtendedTextField', ["u'body'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'body_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'body_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'hierarchy': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']", 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'db_index': 'True'}),
            'sysname': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'db_index': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['site_specific']
