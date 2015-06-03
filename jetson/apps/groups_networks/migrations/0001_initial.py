# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from jetson.apps.groups_networks.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'GroupMembership'
        db.create_table('groups_networks_groupmembership', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('user', models.ForeignKey(orm['auth.User'])),
            ('role', models.CharField(_("Role"), default='members', max_length=30)),
            ('title', MultilingualCharField(_("Title"), max_length=255, blank=True)),
            ('inviter', models.ForeignKey(orm['auth.User'], related_name="group_inviter", null=True, blank=True)),
            ('is_accepted', models.BooleanField(_("Accepted by user"), default=False)),
            ('is_blocked', models.BooleanField(_("Blocked"), default=False)),
            ('is_contact_person', models.BooleanField(_("Contact Person"), default=False)),
            ('confirmer', models.ForeignKey(orm['auth.User'], related_name="group_confirmer", null=True, blank=True)),
            ('timestamp', models.DateTimeField(_("Timestamp"), auto_now_add=True, null=True, editable=False)),
            ('activation', models.DateTimeField(_("Activated"), null=True, editable=False)),
            ('title_de', models.CharField(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('title_en', models.CharField(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('person_group', models.ForeignKey(orm['groups_networks.persongroup'])),
        )))
        db.send_create_signal('groups_networks', ['GroupMembership'])
        
        # Adding model 'PersonGroup'
        db.create_table('groups_networks_persongroup', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('creation_date', models.DateTimeField(_("creation date"), editable=False)),
            ('modified_date', models.DateTimeField(_("modified date"), null=True, editable=False)),
            ('content_type', models.ForeignKey(orm['contenttypes.ContentType'], related_name=None, null=True, blank=True)),
            ('object_id', models.CharField(u'Related object', max_length=255, null=False, blank=True)),
            ('slug', models.SlugField(unique=True, max_length=255)),
            ('title', models.CharField(_("Title"), max_length=255)),
            ('title2', models.CharField(_("Title 2"), max_length=255, blank=True)),
            ('description', MultilingualTextField(_("Description"), blank=True)),
            ('group_type', models.ForeignKey(orm['structure.Term'], limit_choices_to=models.Q(vocabulary__sysname='basics_object_types',path_search__contains=ObjectTypeFilter("person_group"))&~models.Q(models.Q(sysname="person_group")), related_name="type_groups")),
            ('organizing_institution', models.ForeignKey(orm['institutions.Institution'], null=True, blank=True)),
            ('access_type', models.ForeignKey(orm['structure.Term'], limit_choices_to={'vocabulary__sysname':'group_access_types'}, related_name="access_type_groups")),
            ('is_by_invitation', models.BooleanField(_("Membership by Invitation"), default=False)),
            ('is_by_confirmation', models.BooleanField(_("Membership by Confirmation"), default=False)),
            ('preferred_language', models.ForeignKey(orm['i18n.Language'], limit_choices_to={'display':True}, null=True, blank=True)),
            ('status', models.ForeignKey(orm['structure.Term'], limit_choices_to={'vocabulary__sysname':'basics_object_statuses'}, related_name="status_groups", default=DefaultObjectStatus("draft"), blank=True, null=True)),
            ('image', FileBrowseField(_('Image'), extensions=['.jpg','.jpeg','.gif','.png','.tif','.tiff'], max_length=255, directory="/%s/"%URL_ID_PERSONGROUPS, blank=True)),
            ('description_de', ExtendedTextField(u'Description', unique_for_month=None, unique=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, null=False, unique_for_date=None, db_tablespace='', db_index=False)),
            ('description_de_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('description_en', ExtendedTextField(u'Description', unique_for_month=None, unique=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, null=False, unique_for_date=None, db_tablespace='', db_index=False)),
            ('description_en_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('description_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
        )))
        db.send_create_signal('groups_networks', ['PersonGroup'])
        
        # Adding ManyToManyField 'PersonGroup.context_categories'
        db.create_table('groups_networks_persongroup_context_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('persongroup', models.ForeignKey(orm.PersonGroup, null=False)),
            ('contextcategory', models.ForeignKey(orm['structure.ContextCategory'], null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'GroupMembership'
        db.delete_table('groups_networks_groupmembership')
        
        # Deleting model 'PersonGroup'
        db.delete_table('groups_networks_persongroup')
        
        # Dropping ManyToManyField 'PersonGroup.context_categories'
        db.delete_table('groups_networks_persongroup_context_categories')
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'structure.contextcategory': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'structure.term': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'groups_networks.groupmembership': {
            'activation': ('models.DateTimeField', ['_("Activated")'], {'null': 'True', 'editable': 'False'}),
            'confirmer': ('models.ForeignKey', ["orm['auth.User']"], {'related_name': '"group_confirmer"', 'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'inviter': ('models.ForeignKey', ["orm['auth.User']"], {'related_name': '"group_inviter"', 'null': 'True', 'blank': 'True'}),
            'is_accepted': ('models.BooleanField', ['_("Accepted by user")'], {'default': 'False'}),
            'is_blocked': ('models.BooleanField', ['_("Blocked")'], {'default': 'False'}),
            'is_contact_person': ('models.BooleanField', ['_("Contact Person")'], {'default': 'False'}),
            'person_group': ('models.ForeignKey', ["orm['groups_networks.persongroup']"], {}),
            'role': ('models.CharField', ['_("Role")'], {'default': "'members'", 'max_length': '30'}),
            'timestamp': ('models.DateTimeField', ['_("Timestamp")'], {'auto_now_add': 'True', 'null': 'True', 'editable': 'False'}),
            'title': ('MultilingualCharField', ['_("Title")'], {'max_length': '255', 'blank': 'True'}),
            'title_de': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'user': ('models.ForeignKey', ["orm['auth.User']"], {})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'institutions.institution': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'i18n.language': {
            'Meta': {'ordering': "XFieldList(['sort_order','name_'])"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'groups_networks.persongroup': {
            'access_type': ('models.ForeignKey', ["orm['structure.Term']"], {'limit_choices_to': "{'vocabulary__sysname':'group_access_types'}", 'related_name': '"access_type_groups"'}),
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'related_name': 'None', 'null': 'True', 'blank': 'True'}),
            'context_categories': ('models.ManyToManyField', ["orm['structure.ContextCategory']"], {'limit_choices_to': "{'is_applied4persongroup':True}", 'blank': 'True'}),
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'editable': 'False'}),
            'description': ('MultilingualTextField', ['_("Description")'], {'blank': 'True'}),
            'description_de': ('ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'group_type': ('models.ForeignKey', ["orm['structure.Term']"], {'limit_choices_to': 'models.Q(vocabulary__sysname=\'basics_object_types\',path_search__contains=ObjectTypeFilter("person_group"))&~models.Q(models.Q(sysname="person_group"))', 'related_name': '"type_groups"'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'image': ('FileBrowseField', ["_('Image')"], {'extensions': "['.jpg','.jpeg','.gif','.png','.tif','.tiff']", 'max_length': '255', 'directory': '"/%s/"%URL_ID_PERSONGROUPS', 'blank': 'True'}),
            'is_by_confirmation': ('models.BooleanField', ['_("Membership by Confirmation")'], {'default': 'False'}),
            'is_by_invitation': ('models.BooleanField', ['_("Membership by Invitation")'], {'default': 'False'}),
            'modified_date': ('models.DateTimeField', ['_("modified date")'], {'null': 'True', 'editable': 'False'}),
            'object_id': ('models.CharField', ["u'Related object'"], {'max_length': '255', 'null': 'False', 'blank': 'True'}),
            'organizing_institution': ('models.ForeignKey', ["orm['institutions.Institution']"], {'null': 'True', 'blank': 'True'}),
            'preferred_language': ('models.ForeignKey', ["orm['i18n.Language']"], {'limit_choices_to': "{'display':True}", 'null': 'True', 'blank': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'status': ('models.ForeignKey', ["orm['structure.Term']"], {'limit_choices_to': "{'vocabulary__sysname':'basics_object_statuses'}", 'related_name': '"status_groups"', 'default': 'DefaultObjectStatus("draft")', 'blank': 'True', 'null': 'True'}),
            'title': ('models.CharField', ['_("Title")'], {'max_length': '255'}),
            'title2': ('models.CharField', ['_("Title 2")'], {'max_length': '255', 'blank': 'True'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['groups_networks']
