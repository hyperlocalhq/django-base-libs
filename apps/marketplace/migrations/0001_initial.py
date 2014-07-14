# -*- coding: UTF-8 -*-
from django.db import models

from south.db import db

from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

from ccb.apps.people.models import *
from ccb.apps.institutions.models import *
from ccb.apps.marketplace.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'JobType'
        db.create_table('marketplace_jobtype', south_cleaned_fields((
            ('id', orm['marketplace.JobType:id']),
            ('slug', orm['marketplace.JobType:slug']),
            ('title', orm['marketplace.JobType:title']),
            ('sort_order', orm['marketplace.JobType:sort_order']),
            ('title_de', orm['marketplace.JobType:title_de']),
            ('title_en', orm['marketplace.JobType:title_en']),
        )))
        db.send_create_signal('marketplace', ['JobType'])
        
        # Adding model 'JobOffer'
        db.create_table('marketplace_joboffer', south_cleaned_fields((
            ('id', orm['marketplace.JobOffer:id']),
            ('creation_date', orm['marketplace.JobOffer:creation_date']),
            ('modified_date', orm['marketplace.JobOffer:modified_date']),
            ('creator', orm['marketplace.JobOffer:creator']),
            ('modifier', orm['marketplace.JobOffer:modifier']),
            ('author', orm['marketplace.JobOffer:author']),
            ('published_from', orm['marketplace.JobOffer:published_from']),
            ('published_till', orm['marketplace.JobOffer:published_till']),
            ('status', orm['marketplace.JobOffer:status']),
            ('position', orm['marketplace.JobOffer:position']),
            ('description', orm['marketplace.JobOffer:description']),
            ('job_type', orm['marketplace.JobOffer:job_type']),
            ('qualification', orm['marketplace.JobOffer:qualification']),
            ('offering_institution', orm['marketplace.JobOffer:offering_institution']),
            ('offering_institution_title', orm['marketplace.JobOffer:offering_institution_title']),
            ('contact_person', orm['marketplace.JobOffer:contact_person']),
            ('contact_person_name', orm['marketplace.JobOffer:contact_person_name']),
            ('postal_address', orm['marketplace.JobOffer:postal_address']),
            ('additional_info', orm['marketplace.JobOffer:additional_info']),
            ('phone0_type', orm['marketplace.JobOffer:phone0_type']),
            ('phone0_country', orm['marketplace.JobOffer:phone0_country']),
            ('phone0_area', orm['marketplace.JobOffer:phone0_area']),
            ('phone0_number', orm['marketplace.JobOffer:phone0_number']),
            ('is_phone0_default', orm['marketplace.JobOffer:is_phone0_default']),
            ('is_phone0_on_hold', orm['marketplace.JobOffer:is_phone0_on_hold']),
            ('phone1_type', orm['marketplace.JobOffer:phone1_type']),
            ('phone1_country', orm['marketplace.JobOffer:phone1_country']),
            ('phone1_area', orm['marketplace.JobOffer:phone1_area']),
            ('phone1_number', orm['marketplace.JobOffer:phone1_number']),
            ('is_phone1_default', orm['marketplace.JobOffer:is_phone1_default']),
            ('is_phone1_on_hold', orm['marketplace.JobOffer:is_phone1_on_hold']),
            ('phone2_type', orm['marketplace.JobOffer:phone2_type']),
            ('phone2_country', orm['marketplace.JobOffer:phone2_country']),
            ('phone2_area', orm['marketplace.JobOffer:phone2_area']),
            ('phone2_number', orm['marketplace.JobOffer:phone2_number']),
            ('is_phone2_default', orm['marketplace.JobOffer:is_phone2_default']),
            ('is_phone2_on_hold', orm['marketplace.JobOffer:is_phone2_on_hold']),
            ('url0_type', orm['marketplace.JobOffer:url0_type']),
            ('url0_link', orm['marketplace.JobOffer:url0_link']),
            ('is_url0_default', orm['marketplace.JobOffer:is_url0_default']),
            ('is_url0_on_hold', orm['marketplace.JobOffer:is_url0_on_hold']),
            ('url1_type', orm['marketplace.JobOffer:url1_type']),
            ('url1_link', orm['marketplace.JobOffer:url1_link']),
            ('is_url1_default', orm['marketplace.JobOffer:is_url1_default']),
            ('is_url1_on_hold', orm['marketplace.JobOffer:is_url1_on_hold']),
            ('url2_type', orm['marketplace.JobOffer:url2_type']),
            ('url2_link', orm['marketplace.JobOffer:url2_link']),
            ('is_url2_default', orm['marketplace.JobOffer:is_url2_default']),
            ('is_url2_on_hold', orm['marketplace.JobOffer:is_url2_on_hold']),
            ('im0_type', orm['marketplace.JobOffer:im0_type']),
            ('im0_address', orm['marketplace.JobOffer:im0_address']),
            ('is_im0_default', orm['marketplace.JobOffer:is_im0_default']),
            ('is_im0_on_hold', orm['marketplace.JobOffer:is_im0_on_hold']),
            ('im1_type', orm['marketplace.JobOffer:im1_type']),
            ('im1_address', orm['marketplace.JobOffer:im1_address']),
            ('is_im1_default', orm['marketplace.JobOffer:is_im1_default']),
            ('is_im1_on_hold', orm['marketplace.JobOffer:is_im1_on_hold']),
            ('im2_type', orm['marketplace.JobOffer:im2_type']),
            ('im2_address', orm['marketplace.JobOffer:im2_address']),
            ('is_im2_default', orm['marketplace.JobOffer:is_im2_default']),
            ('is_im2_on_hold', orm['marketplace.JobOffer:is_im2_on_hold']),
            ('email0_type', orm['marketplace.JobOffer:email0_type']),
            ('email0_address', orm['marketplace.JobOffer:email0_address']),
            ('is_email0_default', orm['marketplace.JobOffer:is_email0_default']),
            ('is_email0_on_hold', orm['marketplace.JobOffer:is_email0_on_hold']),
            ('email1_type', orm['marketplace.JobOffer:email1_type']),
            ('email1_address', orm['marketplace.JobOffer:email1_address']),
            ('is_email1_default', orm['marketplace.JobOffer:is_email1_default']),
            ('is_email1_on_hold', orm['marketplace.JobOffer:is_email1_on_hold']),
            ('email2_type', orm['marketplace.JobOffer:email2_type']),
            ('email2_address', orm['marketplace.JobOffer:email2_address']),
            ('is_email2_default', orm['marketplace.JobOffer:is_email2_default']),
            ('is_email2_on_hold', orm['marketplace.JobOffer:is_email2_on_hold']),
            ('tags', orm['marketplace.JobOffer:tags']),
        )))
        db.send_create_signal('marketplace', ['JobOffer'])
        
        # Adding model 'JobQualification'
        db.create_table('marketplace_jobqualification', south_cleaned_fields((
            ('id', orm['marketplace.JobQualification:id']),
            ('slug', orm['marketplace.JobQualification:slug']),
            ('title', orm['marketplace.JobQualification:title']),
            ('sort_order', orm['marketplace.JobQualification:sort_order']),
            ('title_de', orm['marketplace.JobQualification:title_de']),
            ('title_en', orm['marketplace.JobQualification:title_en']),
        )))
        db.send_create_signal('marketplace', ['JobQualification'])
        
        # Adding model 'JobSector'
        db.create_table('marketplace_jobsector', south_cleaned_fields((
            ('id', orm['marketplace.JobSector:id']),
            ('slug', orm['marketplace.JobSector:slug']),
            ('title', orm['marketplace.JobSector:title']),
            ('sort_order', orm['marketplace.JobSector:sort_order']),
            ('title_de', orm['marketplace.JobSector:title_de']),
            ('title_en', orm['marketplace.JobSector:title_en']),
        )))
        db.send_create_signal('marketplace', ['JobSector'])
        
        # Adding ManyToManyField 'JobOffer.job_sectors'
        db.create_table('marketplace_joboffer_job_sectors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('joboffer', models.ForeignKey(orm.JobOffer, null=False)),
            ('jobsector', models.ForeignKey(orm.JobSector, null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'JobType'
        db.delete_table('marketplace_jobtype')
        
        # Deleting model 'JobOffer'
        db.delete_table('marketplace_joboffer')
        
        # Deleting model 'JobQualification'
        db.delete_table('marketplace_jobqualification')
        
        # Deleting model 'JobSector'
        db.delete_table('marketplace_jobsector')
        
        # Dropping ManyToManyField 'JobOffer.job_sectors'
        db.delete_table('marketplace_joboffer_job_sectors')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'row_level_permissions_owned': ('django.contrib.contenttypes.generic.GenericRelation', [], {'object_id_field': "'owner_object_id'", 'content_type_field': "'owner_content_type'", 'to': "orm['permissions.RowLevelPermission']"}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'i18n.country': {
            'adm_area': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'iso2_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'unique': 'True', 'primary_key': 'True'}),
            'iso3_code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '56', 'unique': 'True'}),
            'name_de': ('django.db.models.fields.CharField', [], {'max_length': '56', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'sort_order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '20'}),
            'territory_of': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'})
        },
        'i18n.language': {
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso2_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'iso3_code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'unique': 'True'}),
            'name_de': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'sort_order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '20'}),
            'synonym': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'})
        },
        'i18n.nationality': {
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'unique': 'True'}),
            'name_de': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'sort_order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '20'})
        },
        'i18n.timezone': {
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['i18n.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'zone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'unique': 'True'})
        },
        'institutions.institution': {
            'access': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'context_categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['structure.ContextCategory']", 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creative_sectors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['structure.Term']", 'blank': 'True'}),
            'description': ('MultilingualTextField', ['_("Description")'], {'blank': 'True'}),
            'description_de': ('ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'establishment_mm': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'establishment_yyyy': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exceptions': ('MultilingualTextField', ["_('Exceptions for working hours')"], {'blank': 'True'}),
            'exceptions_de': ('ExtendedTextField', ["u'Exceptions for working hours'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'exceptions_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'exceptions_en': ('ExtendedTextField', ["u'Exceptions for working hours'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'exceptions_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'exceptions_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'fri_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'fri_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'fri_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'fri_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('FileBrowseField', ["_('Image')"], {'extensions': "['.jpg','.jpeg','.gif','.png','.tif','.tiff']", 'max_length': '255', 'directory': '"/%s/"%URL_ID_INSTITUTIONS', 'blank': 'True'}),
            'institution_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['structure.Term']"}),
            'is_appointment_based': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_card_americanexpress_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_card_mastercard_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_card_visa_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_cash_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_ec_maestro_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_giropay_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_invoice_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_non_profit': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_on_delivery_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_parking_avail': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_paypal_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_prepayment_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_transaction_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_wlan_avail': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'legal_form': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'legal_form_institution'", 'blank': 'True', 'null': 'True', 'to': "orm['structure.Term']"}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'mon_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'mon_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'mon_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'mon_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'nof_employees': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['institutions.Institution']", 'null': 'True', 'blank': 'True'}),
            'row_level_permissions': ('django.contrib.contenttypes.generic.GenericRelation', [], {'to': "orm['permissions.RowLevelPermission']"}),
            'sat_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'sat_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'sat_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'sat_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'default': '87L', 'related_name': "'status_institution_set'", 'blank': 'True', 'null': 'True', 'to': "orm['structure.Term']"}),
            'sun_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'sun_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'sun_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'sun_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'tax_id_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'thu_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'thu_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'thu_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'thu_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'tue_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'tue_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'tue_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'tue_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'vat_id_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'wed_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'wed_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'wed_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'wed_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'location.address': {
            'city': ('django.db.models.fields.CharField', [], {'default': "'Berlin'", 'max_length': '255', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'default': "'DE'", 'to': "orm['i18n.Country']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'street_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'street_address2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'street_address3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'marketplace.joboffer': {
            'additional_info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'joboffer_author'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'contact_person': ('models.ForeignKey', ["orm['people.Person']"], {'related_name': '"jobs_posted"', 'null': 'True', 'blank': 'True'}),
            'contact_person_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'joboffer_creator'", 'null': 'True', 'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email0_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'email0_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'job_offers0'", 'blank': 'True', 'null': 'True', 'to': "orm['optionset.EmailType']"}),
            'email1_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'email1_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'job_offers1'", 'blank': 'True', 'null': 'True', 'to': "orm['optionset.EmailType']"}),
            'email2_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'email2_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'job_offers2'", 'blank': 'True', 'null': 'True', 'to': "orm['optionset.EmailType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'im0_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'im0_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'job_offers0'", 'blank': 'True', 'null': 'True', 'to': "orm['optionset.IMType']"}),
            'im1_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'im1_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'job_offers1'", 'blank': 'True', 'null': 'True', 'to': "orm['optionset.IMType']"}),
            'im2_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'im2_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'job_offers2'", 'blank': 'True', 'null': 'True', 'to': "orm['optionset.IMType']"}),
            'is_email0_default': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_email0_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_email1_default': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_email1_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_email2_default': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_email2_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_im0_default': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_im0_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_im1_default': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_im1_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_im2_default': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_im2_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_phone0_default': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_phone0_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_phone1_default': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_phone1_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_phone2_default': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_phone2_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_url0_default': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_url0_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_url1_default': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_url1_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_url2_default': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_url2_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'job_sectors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['marketplace.JobSector']", 'blank': 'True'}),
            'job_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['marketplace.JobType']"}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'joboffer_modifier'", 'null': 'True', 'to': "orm['auth.User']"}),
            'offering_institution': ('models.ForeignKey', ["orm['institutions.Institution']"], {'null': 'True', 'blank': 'True'}),
            'offering_institution_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'phone0_area': ('django.db.models.fields.CharField', [], {'default': "'30'", 'max_length': '5', 'blank': 'True'}),
            'phone0_country': ('django.db.models.fields.CharField', [], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'phone0_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'phone0_type': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'job_offers0'", 'blank': 'True', 'null': 'True', 'to': "orm['optionset.PhoneType']"}),
            'phone1_area': ('django.db.models.fields.CharField', [], {'default': "'30'", 'max_length': '5', 'blank': 'True'}),
            'phone1_country': ('django.db.models.fields.CharField', [], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'phone1_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'phone1_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '2L', 'related_name': "'job_offers1'", 'blank': 'True', 'null': 'True', 'to': "orm['optionset.PhoneType']"}),
            'phone2_area': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'phone2_country': ('django.db.models.fields.CharField', [], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'phone2_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'phone2_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '3L', 'related_name': "'job_offers2'", 'blank': 'True', 'null': 'True', 'to': "orm['optionset.PhoneType']"}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'postal_address': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'address_job_offers'", 'blank': 'True', 'null': 'True', 'to': "orm['location.Address']"}),
            'published_from': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'published_till': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'qualification': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['marketplace.JobQualification']"}),
            'row_level_permissions': ('django.contrib.contenttypes.generic.GenericRelation', [], {'to': "orm['permissions.RowLevelPermission']"}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'tags': ('TagField', [], {'blank': 'True'}),
            'url0_link': ('URLField', ['_("URL")'], {'blank': 'True'}),
            'url0_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'job_offers0'", 'blank': 'True', 'null': 'True', 'to': "orm['optionset.URLType']"}),
            'url1_link': ('URLField', ['_("URL")'], {'blank': 'True'}),
            'url1_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'job_offers1'", 'blank': 'True', 'null': 'True', 'to': "orm['optionset.URLType']"}),
            'url2_link': ('URLField', ['_("URL")'], {'blank': 'True'}),
            'url2_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'job_offers2'", 'blank': 'True', 'null': 'True', 'to': "orm['optionset.URLType']"})
        },
        'marketplace.jobqualification': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('MultilingualCharField', ['_("title")'], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'marketplace.jobsector': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('MultilingualCharField', ['_("title")'], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'marketplace.jobtype': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('MultilingualCharField', ['_("title")'], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'optionset.emailtype': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('MultilingualCharField', ["_('title')"], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'optionset.imtype': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('MultilingualCharField', ["_('title')"], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'optionset.phonetype': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('MultilingualCharField', ["_('title')"], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'vcard_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'optionset.prefix': {
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('MultilingualCharField', ["_('title')"], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'optionset.salutation': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'template': ('MultilingualCharField', ["_('template')"], {'max_length': '255'}),
            'template_de': ('models.CharField', ["u'template'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'template_en': ('models.CharField', ["u'template'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title': ('MultilingualCharField', ["_('title')"], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'optionset.urltype': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('MultilingualCharField', ["_('title')"], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'people.person': {
            'allow_search_engine_indexing': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'birthday_dd': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'birthday_mm': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'birthday_yyyy': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'birthname': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'context_categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['structure.ContextCategory']", 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creative_sectors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['structure.Term']", 'blank': 'True'}),
            'degree': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'description': ('MultilingualTextField', ['_("Description")'], {'blank': 'True'}),
            'description_de': ('ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'display_address': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'display_birthday': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'display_email': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'display_fax': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'display_im': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'display_mobile': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'display_phone': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'display_username': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('FileBrowseField', ["_('Image')"], {'extensions': "['.jpg','.jpeg','.gif','.png','.tif','.tiff']", 'max_length': '255', 'directory': '"/%s/"%URL_ID_PEOPLE', 'blank': 'True'}),
            'individual_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structure.Term']", 'null': 'True', 'blank': 'True'}),
            'interests': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'nationality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['i18n.Nationality']", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'occupation': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'preferred_language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['i18n.Language']", 'null': 'True', 'blank': 'True'}),
            'prefix': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['optionset.Prefix']", 'null': 'True', 'blank': 'True'}),
            'row_level_permissions': ('django.contrib.contenttypes.generic.GenericRelation', [], {'to': "orm['permissions.RowLevelPermission']"}),
            'salutation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['optionset.Salutation']", 'null': 'True', 'blank': 'True'}),
            'spoken_languages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['i18n.Language']", 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'default': '87L', 'related_name': "'status_person_set'", 'blank': 'True', 'null': 'True', 'to': "orm['structure.Term']"}),
            'timezone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['i18n.TimeZone']", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'permissions.rowlevelpermission': {
            'Meta': {'db_table': "'auth_rowlevelpermission'"},
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'related_name': 'None', 'null': 'False', 'blank': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'negative': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'object_id': ('models.CharField', ["u'Related object'"], {'max_length': '255', 'null': 'False', 'blank': 'False'}),
            'owner_content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'related_name': "'owner'", 'null': 'False', 'blank': 'False'}),
            'owner_object_id': ('models.CharField', ["u'Owner'"], {'max_length': '255', 'null': 'False', 'blank': 'False'}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.Permission']"})
        },
        'structure.contextcategory': {
            'body': ('MultilingualTextField', ["_('body')"], {'blank': 'True'}),
            'body_de': ('ExtendedTextField', ["u'body'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'body_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'body_en': ('ExtendedTextField', ["u'body'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'body_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'body_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'creative_sectors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['structure.Term']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('FileBrowseField', ["_('Image')"], {'extensions': "['.jpg','.jpeg','.gif','.png','.tif','.tiff']", 'max_length': '255', 'blank': 'True'}),
            'is_applied4document': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_applied4event': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_applied4institution': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_applied4person': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_applied4persongroup': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'child_set'", 'blank': 'True', 'null': 'True', 'to': "orm['structure.ContextCategory']"}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '8192', 'null': 'True'}),
            'path_search': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'sysname': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'title': ('MultilingualCharField', ["_('title')"], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'structure.term': {
            'body': ('MultilingualTextField', ["_('body')"], {'blank': 'True'}),
            'body_de': ('ExtendedTextField', ["u'body'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'body_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'body_en': ('ExtendedTextField', ["u'body'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'body_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'body_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('FileBrowseField', ["_('Image')"], {'extensions': "['.jpg','.jpeg','.gif','.png','.tif','.tiff']", 'max_length': '255', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'child_set'", 'blank': 'True', 'null': 'True', 'to': "orm['structure.Term']"}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '8192', 'null': 'True'}),
            'path_search': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'sysname': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'title': ('MultilingualCharField', ["_('title')"], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'vocabulary': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structure.Vocabulary']"})
        },
        'structure.vocabulary': {
            'body': ('MultilingualTextField', ["_('body')"], {'blank': 'True'}),
            'body_de': ('ExtendedTextField', ["u'body'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'body_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'body_en': ('ExtendedTextField', ["u'body'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'body_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'body_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'hierarchy': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('FileBrowseField', ["_('Image')"], {'extensions': "['.jpg','.jpeg','.gif','.png','.tif','.tiff']", 'max_length': '255', 'blank': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sysname': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'title': ('MultilingualCharField', ["_('title')"], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['marketplace']
