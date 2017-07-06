# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from jetson.apps.individual_relations.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'IndividualRelationType'
        db.create_table('individual_relations_individualrelationtype', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('sort_order', models.IntegerField(_("sort order"), editable=False, blank=True)),
            ('parent', models.ForeignKey(orm.IndividualRelationType, related_name="child_set", null=True, blank=True)),
            ('path', models.CharField(_('path'), editable=False, max_length=8192, null=True)),
            ('slug', models.SlugField(unique=True, max_length=255)),
            ('title', MultilingualCharField(_('title'), max_length=255)),
            ('backwards', models.ForeignKey(orm.IndividualRelationType, related_name="backwards_relation_set", null=True, blank=True)),
            ('title_de', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('title_en', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
        )))
        db.send_create_signal('individual_relations', ['IndividualRelationType'])
        
        # Adding model 'IndividualRelation'
        db.create_table('individual_relations_individualrelation', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('user', models.ForeignKey(orm['auth.User'])),
            ('to_user', models.ForeignKey(orm['auth.User'], related_name="to_user")),
            ('timestamp', models.DateTimeField(_("Created"), auto_now_add=True, null=True, editable=False)),
            ('activation', models.DateTimeField(_("Activated"), null=True, editable=False)),
            ('status', models.CharField(_("Status of the user #1"), max_length=10)),
            ('display_birthday', models.BooleanField(_("Display birthday to user #2"), default=True)),
            ('display_address', models.BooleanField(_("Display address data to user #2"), default=True)),
            ('display_phone', models.BooleanField(_("Display phone numbers to user #2"), default=True)),
            ('display_fax', models.BooleanField(_("Display fax numbers to user #2"), default=True)),
            ('display_mobile', models.BooleanField(_("Display mobile phones to user #2"), default=True)),
            ('display_im', models.BooleanField(_("Display instant messengers to user #2"), default=True)),
            ('message', models.TextField(_("Message from user #1 to user #2"), blank=True)),
        )))
        db.send_create_signal('individual_relations', ['IndividualRelation'])
        
        # Adding ManyToManyField 'IndividualRelation.relation_types'
        db.create_table('individual_relations_individualrelation_relation_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('individualrelation', models.ForeignKey(orm.IndividualRelation, null=False)),
            ('individualrelationtype', models.ForeignKey(orm.IndividualRelationType, null=False))
        ))
        
        # Creating unique_together for [user, to_user] on IndividualRelation.
        db.create_unique('individual_relations_individualrelation', ['user_id', 'to_user_id'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'IndividualRelationType'
        db.delete_table('individual_relations_individualrelationtype')
        
        # Deleting model 'IndividualRelation'
        db.delete_table('individual_relations_individualrelation')
        
        # Dropping ManyToManyField 'IndividualRelation.relation_types'
        db.delete_table('individual_relations_individualrelation_relation_types')
        
        # Deleting unique_together for [user, to_user] on IndividualRelation.
        db.delete_unique('individual_relations_individualrelation', ['user_id', 'to_user_id'])
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'individual_relations.individualrelationtype': {
            'backwards': ('models.ForeignKey', ["orm['individual_relations.IndividualRelationType']"], {'related_name': '"backwards_relation_set"', 'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'parent': ('models.ForeignKey', ["orm['individual_relations.IndividualRelationType']"], {'related_name': '"child_set"', 'null': 'True', 'blank': 'True'}),
            'path': ('models.CharField', ["_('path')"], {'editable': 'False', 'max_length': '8192', 'null': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('models.IntegerField', ['_("sort order")'], {'editable': 'False', 'blank': 'True'}),
            'title': ('MultilingualCharField', ["_('title')"], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'individual_relations.individualrelation': {
            'Meta': {'unique_together': '(("user","to_user"),)'},
            'activation': ('models.DateTimeField', ['_("Activated")'], {'null': 'True', 'editable': 'False'}),
            'display_address': ('models.BooleanField', ['_("Display address data to user #2")'], {'default': 'True'}),
            'display_birthday': ('models.BooleanField', ['_("Display birthday to user #2")'], {'default': 'True'}),
            'display_fax': ('models.BooleanField', ['_("Display fax numbers to user #2")'], {'default': 'True'}),
            'display_im': ('models.BooleanField', ['_("Display instant messengers to user #2")'], {'default': 'True'}),
            'display_mobile': ('models.BooleanField', ['_("Display mobile phones to user #2")'], {'default': 'True'}),
            'display_phone': ('models.BooleanField', ['_("Display phone numbers to user #2")'], {'default': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'message': ('models.TextField', ['_("Message from user #1 to user #2")'], {'blank': 'True'}),
            'relation_types': ('models.ManyToManyField', ["orm['individual_relations.IndividualRelationType']"], {'blank': 'True'}),
            'status': ('models.CharField', ['_("Status of the user #1")'], {'max_length': '10'}),
            'timestamp': ('models.DateTimeField', ['_("Created")'], {'auto_now_add': 'True', 'null': 'True', 'editable': 'False'}),
            'to_user': ('models.ForeignKey', ["orm['auth.User']"], {'related_name': '"to_user"'}),
            'user': ('models.ForeignKey', ["orm['auth.User']"], {})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['individual_relations']
