# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'JobType.is_internship'
        db.add_column('marketplace_jobtype', 'is_internship', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True), keep_default=False)

        # Changing field 'JobType.title'
        db.alter_column('marketplace_jobtype', 'title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True))

        # Adding field 'JobOffer.is_commercial'
        db.add_column('marketplace_joboffer', 'is_commercial', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True), keep_default=False)

        # Adding field 'JobOffer.publish_emails'
        db.add_column('marketplace_joboffer', 'publish_emails', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True), keep_default=False)

        # Changing field 'JobOffer.url1_link'
        db.alter_column('marketplace_joboffer', 'url1_link', self.gf('base_libs.models.fields.URLField')(max_length=200, blank=True))

        # Changing field 'JobOffer.url0_link'
        db.alter_column('marketplace_joboffer', 'url0_link', self.gf('base_libs.models.fields.URLField')(max_length=200, blank=True))

        # Changing field 'JobOffer.tags'
        db.alter_column('marketplace_joboffer', 'tags', self.gf('tagging_autocomplete.models.TagAutocompleteField')())

        # Changing field 'JobOffer.url2_link'
        db.alter_column('marketplace_joboffer', 'url2_link', self.gf('base_libs.models.fields.URLField')(max_length=200, blank=True))

        # Changing field 'JobSector.title'
        db.alter_column('marketplace_jobsector', 'title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True))

        # Changing field 'JobQualification.title'
        db.alter_column('marketplace_jobqualification', 'title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True))
    
    
    def backwards(self, orm):
        
        # Deleting field 'JobType.is_internship'
        db.delete_column('marketplace_jobtype', 'is_internship')

        # Changing field 'JobType.title'
        db.alter_column('marketplace_jobtype', 'title', self.gf('MultilingualCharField')(_("title"), max_length=255))

        # Deleting field 'JobOffer.is_commercial'
        db.delete_column('marketplace_joboffer', 'is_commercial')

        # Deleting field 'JobOffer.publish_emails'
        db.delete_column('marketplace_joboffer', 'publish_emails')

        # Changing field 'JobOffer.url1_link'
        db.alter_column('marketplace_joboffer', 'url1_link', self.gf('URLField')(_("URL"), blank=True))

        # Changing field 'JobOffer.url0_link'
        db.alter_column('marketplace_joboffer', 'url0_link', self.gf('URLField')(_("URL"), blank=True))

        # Changing field 'JobOffer.tags'
        db.alter_column('marketplace_joboffer', 'tags', self.gf('TagField')(blank=True))

        # Changing field 'JobOffer.url2_link'
        db.alter_column('marketplace_joboffer', 'url2_link', self.gf('URLField')(_("URL"), blank=True))

        # Changing field 'JobSector.title'
        db.alter_column('marketplace_jobsector', 'title', self.gf('MultilingualCharField')(_("title"), max_length=255))

        # Changing field 'JobQualification.title'
        db.alter_column('marketplace_jobqualification', 'title', self.gf('MultilingualCharField')(_("title"), max_length=255))
    
    
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
        'i18n.country': {
            'Meta': {'object_name': 'Country'},
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
            'Meta': {'object_name': 'Language'},
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
            'Meta': {'object_name': 'Nationality'},
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'unique': 'True'}),
            'name_de': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'sort_order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '20'})
        },
        'i18n.timezone': {
            'Meta': {'object_name': 'TimeZone'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['i18n.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'zone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'unique': 'True'})
        },
        'institutions.institution': {
            'Meta': {'object_name': 'Institution'},
            'access': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'context_categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['structure.ContextCategory']", 'symmetrical': 'False', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creative_sectors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'creative_sector_institutions'", 'blank': 'True', 'to': "orm['structure.Term']"}),
            'description': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'description_de': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'establishment_mm': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'establishment_yyyy': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exceptions': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'exceptions_de': ('base_libs.models.fields.ExtendedTextField', ["u'Exceptions for working hours'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'exceptions_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'exceptions_en': ('base_libs.models.fields.ExtendedTextField', ["u'Exceptions for working hours'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'exceptions_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'exceptions_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'fri_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'fri_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'fri_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'fri_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'directory': "'/institutions/'", 'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']", 'blank': 'True'}),
            'institution_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['structure.Term']", 'symmetrical': 'False'}),
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
            'Meta': {'object_name': 'Address'},
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
            'Meta': {'object_name': 'JobOffer'},
            'additional_info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'joboffer_author'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'contact_person': ('django.db.models.fields.related.ForeignKey', ["orm['people.Person']"], {'related_name': '"jobs_posted"', 'null': 'True', 'blank': 'True'}),
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
            'is_commercial': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
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
            'job_sectors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'job_sector_joboffers'", 'blank': 'True', 'to': "orm['marketplace.JobSector']"}),
            'job_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['marketplace.JobType']"}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'joboffer_modifier'", 'null': 'True', 'to': "orm['auth.User']"}),
            'offering_institution': ('django.db.models.fields.related.ForeignKey', ["orm['institutions.Institution']"], {'null': 'True', 'blank': 'True'}),
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
            'publish_emails': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'published_from': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'published_till': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'qualifications': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'joboffers'", 'blank': 'True', 'to': "orm['marketplace.JobQualification']"}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'tags': ('tagging_autocomplete.models.TagAutocompleteField', [], {}),
            'url0_link': ('base_libs.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'url0_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'job_offers0'", 'blank': 'True', 'null': 'True', 'to': "orm['optionset.URLType']"}),
            'url1_link': ('base_libs.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'url1_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'job_offers1'", 'blank': 'True', 'null': 'True', 'to': "orm['optionset.URLType']"}),
            'url2_link': ('base_libs.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'url2_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'job_offers2'", 'blank': 'True', 'null': 'True', 'to': "orm['optionset.URLType']"})
        },
        'marketplace.jobqualification': {
            'Meta': {'object_name': 'JobQualification'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'marketplace.jobsector': {
            'Meta': {'object_name': 'JobSector'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'marketplace.jobtype': {
            'Meta': {'object_name': 'JobType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_internship': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'optionset.emailtype': {
            'Meta': {'object_name': 'EmailType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'optionset.imtype': {
            'Meta': {'object_name': 'IMType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'optionset.phonetype': {
            'Meta': {'object_name': 'PhoneType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'vcard_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'optionset.prefix': {
            'Meta': {'object_name': 'Prefix'},
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'optionset.salutation': {
            'Meta': {'object_name': 'Salutation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'template': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'template_de': ('django.db.models.fields.CharField', ["u'template'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'template_en': ('django.db.models.fields.CharField', ["u'template'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'optionset.urltype': {
            'Meta': {'object_name': 'URLType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'people.person': {
            'Meta': {'object_name': 'Person'},
            'allow_search_engine_indexing': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'birthday_dd': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'birthday_mm': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'birthday_yyyy': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'birthname': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'context_categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['structure.ContextCategory']", 'symmetrical': 'False', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creative_sectors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'creative_industry_people'", 'blank': 'True', 'to': "orm['structure.Term']"}),
            'degree': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'description': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'description_de': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
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
            'image': ('filebrowser.fields.FileBrowseField', [], {'directory': "'/people/'", 'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']", 'blank': 'True'}),
            'individual_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structure.Term']", 'null': 'True', 'blank': 'True'}),
            'interests': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'nationality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['i18n.Nationality']", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'occupation': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'preferred_language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['i18n.Language']", 'null': 'True', 'blank': 'True'}),
            'prefix': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['optionset.Prefix']", 'null': 'True', 'blank': 'True'}),
            'salutation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['optionset.Salutation']", 'null': 'True', 'blank': 'True'}),
            'spoken_languages': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'speaking_people'", 'blank': 'True', 'to': "orm['i18n.Language']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'default': '87L', 'related_name': "'status_person_set'", 'blank': 'True', 'null': 'True', 'to': "orm['structure.Term']"}),
            'timezone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['i18n.TimeZone']", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
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
    
    complete_apps = ['marketplace']
