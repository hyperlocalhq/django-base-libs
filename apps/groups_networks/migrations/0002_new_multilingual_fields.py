# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from ccb.apps.groups_networks.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'PersonGroup.description_en_markup_type'
        db.add_column('groups_networks_persongroup', 'description_en_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False))
        
        # Adding field 'PersonGroup.description_markup_type'
        db.add_column('groups_networks_persongroup', 'description_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False))
        
        # Adding field 'PersonGroup.description_de_markup_type'
        db.add_column('groups_networks_persongroup', 'description_de_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False))
        
        # Adding field 'GroupMembership.title_en'
        db.add_column('groups_networks_groupmembership', 'title_en', models.CharField(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False))
        
        # Adding field 'PersonGroup.description_en'
        db.add_column('groups_networks_persongroup', 'description_en', ExtendedTextField(u'Description', unique_for_month=None, unique=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, null=False, unique_for_date=None, db_tablespace='', db_index=False))
        
        # Changing field 'GroupMembership.title_de'
        db.alter_column('groups_networks_groupmembership', 'title_de', models.CharField(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False))
        
        # Changing field 'GroupMembership.title'
        db.alter_column('groups_networks_groupmembership', 'title', MultilingualCharField(_("Title"), max_length=255, blank=True))
        
        # Changing field 'PersonGroup.description_de'
        db.alter_column('groups_networks_persongroup', 'description_de', ExtendedTextField(u'Description', unique_for_month=None, unique=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, null=False, unique_for_date=None, db_tablespace='', db_index=False))
        
        # Changing field 'PersonGroup.description'
        db.alter_column('groups_networks_persongroup', 'description', MultilingualTextField(_("Description"), blank=True))
        
        # Changing field 'PersonGroup.content_type'
        db.alter_column('groups_networks_persongroup', 'content_type_id', models.ForeignKey(orm['contenttypes.ContentType'], null=True, blank=True))
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'PersonGroup.description_en_markup_type'
        db.delete_column('groups_networks_persongroup', 'description_en_markup_type')
        
        # Deleting field 'PersonGroup.description_markup_type'
        db.delete_column('groups_networks_persongroup', 'description_markup_type')
        
        # Deleting field 'PersonGroup.description_de_markup_type'
        db.delete_column('groups_networks_persongroup', 'description_de_markup_type')
        
        # Deleting field 'GroupMembership.title_en'
        db.delete_column('groups_networks_groupmembership', 'title_en')
        
        # Deleting field 'PersonGroup.description_en'
        db.delete_column('groups_networks_persongroup', 'description_en')
        
        # Changing field 'GroupMembership.title_de'
        db.alter_column('groups_networks_groupmembership', 'title_de', models.CharField(_("Title (German)"), max_length=255, blank=True))
        
        # Changing field 'GroupMembership.title'
        db.alter_column('groups_networks_groupmembership', 'title', models.CharField(_("Title (English)"), max_length=255, blank=True))
        
        # Changing field 'PersonGroup.description_de'
        db.alter_column('groups_networks_persongroup', 'description_de', models.TextField(_("Description (German)"), blank=True))
        
        # Changing field 'PersonGroup.description'
        db.alter_column('groups_networks_persongroup', 'description', models.TextField(_("Description (English)"), blank=True))
        
        # Changing field 'PersonGroup.content_type'
        db.alter_column('groups_networks_persongroup', 'content_type_id', models.ForeignKey(orm['contenttypes.ContentType'], limit_choices_to={'model__in': ('address', 'institution')}, null=True, blank=True))
        
    
    
    models = {
        'structure.contextcategory': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'institutions.institution': {
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
            'creative_sectors': ('models.ManyToManyField', ["orm['structure.Term']"], {'limit_choices_to': "{'vocabulary__sysname':'categories_creativesectors'}", 'related_name': '"creative_industry_groups"', 'blank': 'True'}),
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
