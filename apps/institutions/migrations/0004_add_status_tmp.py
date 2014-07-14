# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'Institution.status_tmp'
        db.add_column('institutions_institution', 'status_tmp', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True), keep_default=False)

        # Changing field 'Institution.is_on_delivery_ok'
        db.alter_column('institutions_institution', 'is_on_delivery_ok', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Institution.tax_id_number'
        db.alter_column('institutions_institution', 'tax_id_number', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Institution.parent'
        db.alter_column('institutions_institution', 'parent_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['institutions.Institution'], null=True))

        # Changing field 'Institution.sat_break_open'
        db.alter_column('institutions_institution', 'sat_break_open', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Institution.fri_close'
        db.alter_column('institutions_institution', 'fri_close', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Institution.image'
        db.alter_column('institutions_institution', 'image', self.gf('filebrowser.fields.FileBrowseField')(directory='/institutions/', max_length=255, extensions=['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']))

        # Changing field 'Institution.is_paypal_ok'
        db.alter_column('institutions_institution', 'is_paypal_ok', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Institution.fri_open'
        db.alter_column('institutions_institution', 'fri_open', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Institution.is_parking_avail'
        db.alter_column('institutions_institution', 'is_parking_avail', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Institution.tue_close'
        db.alter_column('institutions_institution', 'tue_close', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Institution.creation_date'
        db.alter_column('institutions_institution', 'creation_date', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Institution.is_invoice_ok'
        db.alter_column('institutions_institution', 'is_invoice_ok', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Institution.sun_break_open'
        db.alter_column('institutions_institution', 'sun_break_open', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Institution.sun_break_close'
        db.alter_column('institutions_institution', 'sun_break_close', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Institution.exceptions_de'
        db.alter_column('institutions_institution', 'exceptions_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Sonstige \xd6ffnungszeiten', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, unique=False, db_tablespace=''))

        # Changing field 'Institution.tue_open'
        db.alter_column('institutions_institution', 'tue_open', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Institution.description_de'
        db.alter_column('institutions_institution', 'description_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Beschreibung', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, unique=False, db_tablespace=''))

        # Changing field 'Institution.is_non_profit'
        db.alter_column('institutions_institution', 'is_non_profit', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Institution.thu_break_open'
        db.alter_column('institutions_institution', 'thu_break_open', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Institution.wed_open'
        db.alter_column('institutions_institution', 'wed_open', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Institution.is_giropay_ok'
        db.alter_column('institutions_institution', 'is_giropay_ok', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Institution.modified_date'
        db.alter_column('institutions_institution', 'modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Institution.mon_close'
        db.alter_column('institutions_institution', 'mon_close', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Institution.mon_break_close'
        db.alter_column('institutions_institution', 'mon_break_close', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Institution.is_transaction_ok'
        db.alter_column('institutions_institution', 'is_transaction_ok', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Institution.sat_close'
        db.alter_column('institutions_institution', 'sat_close', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Institution.sun_open'
        db.alter_column('institutions_institution', 'sun_open', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Institution.tue_break_close'
        db.alter_column('institutions_institution', 'tue_break_close', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Institution.vat_id_number'
        db.alter_column('institutions_institution', 'vat_id_number', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Institution.title'
        db.alter_column('institutions_institution', 'title', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Institution.wed_break_open'
        db.alter_column('institutions_institution', 'wed_break_open', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Institution.sun_close'
        db.alter_column('institutions_institution', 'sun_close', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Institution.sat_break_close'
        db.alter_column('institutions_institution', 'sat_break_close', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Institution.fri_break_close'
        db.alter_column('institutions_institution', 'fri_break_close', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Institution.is_prepayment_ok'
        db.alter_column('institutions_institution', 'is_prepayment_ok', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Institution.description'
        db.alter_column('institutions_institution', 'description', self.gf('base_libs.models.fields.MultilingualTextField')(null=True))

        # Changing field 'Institution.is_wlan_avail'
        db.alter_column('institutions_institution', 'is_wlan_avail', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Institution.thu_close'
        db.alter_column('institutions_institution', 'thu_close', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Institution.thu_open'
        db.alter_column('institutions_institution', 'thu_open', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Institution.description_en'
        db.alter_column('institutions_institution', 'description_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Beschreibung', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, unique=False, db_tablespace=''))

        # Changing field 'Institution.wed_break_close'
        db.alter_column('institutions_institution', 'wed_break_close', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Institution.is_card_mastercard_ok'
        db.alter_column('institutions_institution', 'is_card_mastercard_ok', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Institution.legal_form'
        db.alter_column('institutions_institution', 'legal_form_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['structure.Term']))

        # Changing field 'Institution.is_cash_ok'
        db.alter_column('institutions_institution', 'is_cash_ok', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Institution.exceptions_en'
        db.alter_column('institutions_institution', 'exceptions_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Sonstige \xd6ffnungszeiten', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, unique=False, db_tablespace=''))

        # Changing field 'Institution.fri_break_open'
        db.alter_column('institutions_institution', 'fri_break_open', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Institution.slug'
        db.alter_column('institutions_institution', 'slug', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Institution.mon_open'
        db.alter_column('institutions_institution', 'mon_open', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Institution.is_ec_maestro_ok'
        db.alter_column('institutions_institution', 'is_ec_maestro_ok', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Institution.establishment_mm'
        db.alter_column('institutions_institution', 'establishment_mm', self.gf('django.db.models.fields.SmallIntegerField')(null=True))

        # Changing field 'Institution.sat_open'
        db.alter_column('institutions_institution', 'sat_open', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Institution.access'
        db.alter_column('institutions_institution', 'access', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Institution.is_appointment_based'
        db.alter_column('institutions_institution', 'is_appointment_based', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Institution.wed_close'
        db.alter_column('institutions_institution', 'wed_close', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Institution.nof_employees'
        db.alter_column('institutions_institution', 'nof_employees', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Institution.status'
        db.alter_column('institutions_institution', 'status_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['structure.Term']))

        # Changing field 'Institution.establishment_yyyy'
        db.alter_column('institutions_institution', 'establishment_yyyy', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Institution.tue_break_open'
        db.alter_column('institutions_institution', 'tue_break_open', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Institution.exceptions'
        db.alter_column('institutions_institution', 'exceptions', self.gf('base_libs.models.fields.MultilingualTextField')(null=True))

        # Changing field 'Institution.is_card_americanexpress_ok'
        db.alter_column('institutions_institution', 'is_card_americanexpress_ok', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Institution.mon_break_open'
        db.alter_column('institutions_institution', 'mon_break_open', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Institution.is_card_visa_ok'
        db.alter_column('institutions_institution', 'is_card_visa_ok', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Institution.title2'
        db.alter_column('institutions_institution', 'title2', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Institution.thu_break_close'
        db.alter_column('institutions_institution', 'thu_break_close', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'InstitutionalContact.is_phone2_on_hold'
        db.alter_column('institutions_institutionalcontact', 'is_phone2_on_hold', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'InstitutionalContact.is_im0_default'
        db.alter_column('institutions_institutionalcontact', 'is_im0_default', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'InstitutionalContact.email0_type'
        db.alter_column('institutions_institutionalcontact', 'email0_type_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['optionset.EmailType']))

        # Changing field 'InstitutionalContact.is_im2_default'
        db.alter_column('institutions_institutionalcontact', 'is_im2_default', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'InstitutionalContact.validity_end_mm'
        db.alter_column('institutions_institutionalcontact', 'validity_end_mm', self.gf('django.db.models.fields.SmallIntegerField')(null=True))

        # Changing field 'InstitutionalContact.is_url0_default'
        db.alter_column('institutions_institutionalcontact', 'is_url0_default', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'InstitutionalContact.is_primary'
        db.alter_column('institutions_institutionalcontact', 'is_primary', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'InstitutionalContact.is_url2_default'
        db.alter_column('institutions_institutionalcontact', 'is_url2_default', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'InstitutionalContact.phone1_type'
        db.alter_column('institutions_institutionalcontact', 'phone1_type_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['optionset.PhoneType']))

        # Changing field 'InstitutionalContact.institution'
        db.alter_column('institutions_institutionalcontact', 'institution_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['institutions.Institution']))

        # Changing field 'InstitutionalContact.is_url1_on_hold'
        db.alter_column('institutions_institutionalcontact', 'is_url1_on_hold', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'InstitutionalContact.is_phone0_default'
        db.alter_column('institutions_institutionalcontact', 'is_phone0_default', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'InstitutionalContact.url1_link'
        db.alter_column('institutions_institutionalcontact', 'url1_link', self.gf('base_libs.models.fields.URLField')(max_length=200))

        # Changing field 'InstitutionalContact.validity_start_yyyy'
        db.alter_column('institutions_institutionalcontact', 'validity_start_yyyy', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'InstitutionalContact.email1_type'
        db.alter_column('institutions_institutionalcontact', 'email1_type_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['optionset.EmailType']))

        # Changing field 'InstitutionalContact.phone0_type'
        db.alter_column('institutions_institutionalcontact', 'phone0_type_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['optionset.PhoneType']))

        # Changing field 'InstitutionalContact.phone2_country'
        db.alter_column('institutions_institutionalcontact', 'phone2_country', self.gf('django.db.models.fields.CharField')(max_length=4))

        # Changing field 'InstitutionalContact.im1_type'
        db.alter_column('institutions_institutionalcontact', 'im1_type_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['optionset.IMType']))

        # Changing field 'InstitutionalContact.im2_type'
        db.alter_column('institutions_institutionalcontact', 'im2_type_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['optionset.IMType']))

        # Changing field 'InstitutionalContact.is_im1_default'
        db.alter_column('institutions_institutionalcontact', 'is_im1_default', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'InstitutionalContact.is_url2_on_hold'
        db.alter_column('institutions_institutionalcontact', 'is_url2_on_hold', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'InstitutionalContact.is_phone2_default'
        db.alter_column('institutions_institutionalcontact', 'is_phone2_default', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'InstitutionalContact.phone1_country'
        db.alter_column('institutions_institutionalcontact', 'phone1_country', self.gf('django.db.models.fields.CharField')(max_length=4))

        # Changing field 'InstitutionalContact.im0_type'
        db.alter_column('institutions_institutionalcontact', 'im0_type_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['optionset.IMType']))

        # Changing field 'InstitutionalContact.url0_type'
        db.alter_column('institutions_institutionalcontact', 'url0_type_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['optionset.URLType']))

        # Changing field 'InstitutionalContact.is_phone0_on_hold'
        db.alter_column('institutions_institutionalcontact', 'is_phone0_on_hold', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'InstitutionalContact.validity_start_mm'
        db.alter_column('institutions_institutionalcontact', 'validity_start_mm', self.gf('django.db.models.fields.SmallIntegerField')(null=True))

        # Changing field 'InstitutionalContact.is_email1_default'
        db.alter_column('institutions_institutionalcontact', 'is_email1_default', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'InstitutionalContact.email2_type'
        db.alter_column('institutions_institutionalcontact', 'email2_type_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['optionset.EmailType']))

        # Changing field 'InstitutionalContact.validity_start_dd'
        db.alter_column('institutions_institutionalcontact', 'validity_start_dd', self.gf('django.db.models.fields.SmallIntegerField')(null=True))

        # Changing field 'InstitutionalContact.is_email0_on_hold'
        db.alter_column('institutions_institutionalcontact', 'is_email0_on_hold', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'InstitutionalContact.is_im2_on_hold'
        db.alter_column('institutions_institutionalcontact', 'is_im2_on_hold', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'InstitutionalContact.is_email2_default'
        db.alter_column('institutions_institutionalcontact', 'is_email2_default', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'InstitutionalContact.email0_address'
        db.alter_column('institutions_institutionalcontact', 'email0_address', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'InstitutionalContact.url2_type'
        db.alter_column('institutions_institutionalcontact', 'url2_type_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['optionset.URLType']))

        # Changing field 'InstitutionalContact.phone0_area'
        db.alter_column('institutions_institutionalcontact', 'phone0_area', self.gf('django.db.models.fields.CharField')(max_length=5))

        # Changing field 'InstitutionalContact.im1_address'
        db.alter_column('institutions_institutionalcontact', 'im1_address', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'InstitutionalContact.postal_address'
        db.alter_column('institutions_institutionalcontact', 'postal_address_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['location.Address']))

        # Changing field 'InstitutionalContact.is_email2_on_hold'
        db.alter_column('institutions_institutionalcontact', 'is_email2_on_hold', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'InstitutionalContact.phone0_country'
        db.alter_column('institutions_institutionalcontact', 'phone0_country', self.gf('django.db.models.fields.CharField')(max_length=4))

        # Changing field 'InstitutionalContact.is_billing_address'
        db.alter_column('institutions_institutionalcontact', 'is_billing_address', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'InstitutionalContact.im2_address'
        db.alter_column('institutions_institutionalcontact', 'im2_address', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'InstitutionalContact.location_title'
        db.alter_column('institutions_institutionalcontact', 'location_title', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'InstitutionalContact.validity_end_yyyy'
        db.alter_column('institutions_institutionalcontact', 'validity_end_yyyy', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'InstitutionalContact.im0_address'
        db.alter_column('institutions_institutionalcontact', 'im0_address', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'InstitutionalContact.email1_address'
        db.alter_column('institutions_institutionalcontact', 'email1_address', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'InstitutionalContact.location_type'
        db.alter_column('institutions_institutionalcontact', 'location_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['optionset.InstitutionalLocationType']))

        # Changing field 'InstitutionalContact.url1_type'
        db.alter_column('institutions_institutionalcontact', 'url1_type_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['optionset.URLType']))

        # Changing field 'InstitutionalContact.email2_address'
        db.alter_column('institutions_institutionalcontact', 'email2_address', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'InstitutionalContact.is_email0_default'
        db.alter_column('institutions_institutionalcontact', 'is_email0_default', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'InstitutionalContact.is_phone1_on_hold'
        db.alter_column('institutions_institutionalcontact', 'is_phone1_on_hold', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'InstitutionalContact.validity_end_dd'
        db.alter_column('institutions_institutionalcontact', 'validity_end_dd', self.gf('django.db.models.fields.SmallIntegerField')(null=True))

        # Changing field 'InstitutionalContact.phone2_type'
        db.alter_column('institutions_institutionalcontact', 'phone2_type_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['optionset.PhoneType']))

        # Changing field 'InstitutionalContact.is_url1_default'
        db.alter_column('institutions_institutionalcontact', 'is_url1_default', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'InstitutionalContact.url2_link'
        db.alter_column('institutions_institutionalcontact', 'url2_link', self.gf('base_libs.models.fields.URLField')(max_length=200))

        # Changing field 'InstitutionalContact.phone0_number'
        db.alter_column('institutions_institutionalcontact', 'phone0_number', self.gf('django.db.models.fields.CharField')(max_length=15))

        # Changing field 'InstitutionalContact.is_email1_on_hold'
        db.alter_column('institutions_institutionalcontact', 'is_email1_on_hold', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'InstitutionalContact.is_im0_on_hold'
        db.alter_column('institutions_institutionalcontact', 'is_im0_on_hold', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'InstitutionalContact.phone1_number'
        db.alter_column('institutions_institutionalcontact', 'phone1_number', self.gf('django.db.models.fields.CharField')(max_length=15))

        # Changing field 'InstitutionalContact.is_shipping_address'
        db.alter_column('institutions_institutionalcontact', 'is_shipping_address', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'InstitutionalContact.phone1_area'
        db.alter_column('institutions_institutionalcontact', 'phone1_area', self.gf('django.db.models.fields.CharField')(max_length=5))

        # Changing field 'InstitutionalContact.is_im1_on_hold'
        db.alter_column('institutions_institutionalcontact', 'is_im1_on_hold', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'InstitutionalContact.is_url0_on_hold'
        db.alter_column('institutions_institutionalcontact', 'is_url0_on_hold', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'InstitutionalContact.phone2_area'
        db.alter_column('institutions_institutionalcontact', 'phone2_area', self.gf('django.db.models.fields.CharField')(max_length=5))

        # Changing field 'InstitutionalContact.phone2_number'
        db.alter_column('institutions_institutionalcontact', 'phone2_number', self.gf('django.db.models.fields.CharField')(max_length=15))

        # Changing field 'InstitutionalContact.is_temporary'
        db.alter_column('institutions_institutionalcontact', 'is_temporary', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'InstitutionalContact.is_phone1_default'
        db.alter_column('institutions_institutionalcontact', 'is_phone1_default', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'InstitutionalContact.url0_link'
        db.alter_column('institutions_institutionalcontact', 'url0_link', self.gf('base_libs.models.fields.URLField')(max_length=200))
    
    
    def backwards(self, orm):
        
        # Deleting field 'Institution.status_tmp'
        db.delete_column('institutions_institution', 'status_tmp')

        # Changing field 'Institution.is_on_delivery_ok'
        db.alter_column('institutions_institution', 'is_on_delivery_ok', self.gf('models.BooleanField')(_("Payment on delivery")))

        # Changing field 'Institution.tax_id_number'
        db.alter_column('institutions_institution', 'tax_id_number', self.gf('models.CharField')(_("Tax ID"), max_length=100))

        # Changing field 'Institution.parent'
        db.alter_column('institutions_institution', 'parent_id', self.gf('models.ForeignKey')(orm['institutions.Institution'], null=True))

        # Changing field 'Institution.sat_break_open'
        db.alter_column('institutions_institution', 'sat_break_open', self.gf('models.TimeField')(_('Break Ends on Saturday'), null=True))

        # Changing field 'Institution.fri_close'
        db.alter_column('institutions_institution', 'fri_close', self.gf('models.TimeField')(_('Closes on Friday'), null=True))

        # Changing field 'Institution.image'
        db.alter_column('institutions_institution', 'image', self.gf('FileBrowseField')(_('Image'), directory="/%s/"%URL_ID_INSTITUTIONS, max_length=255, extensions=['.jpg','.jpeg','.gif','.png','.tif','.tiff']))

        # Changing field 'Institution.is_paypal_ok'
        db.alter_column('institutions_institution', 'is_paypal_ok', self.gf('models.BooleanField')(_("PayPal")))

        # Changing field 'Institution.fri_open'
        db.alter_column('institutions_institution', 'fri_open', self.gf('models.TimeField')(_('Opens on Friday'), null=True))

        # Changing field 'Institution.is_parking_avail'
        db.alter_column('institutions_institution', 'is_parking_avail', self.gf('models.BooleanField')(_("Is parking available?")))

        # Changing field 'Institution.tue_close'
        db.alter_column('institutions_institution', 'tue_close', self.gf('models.TimeField')(_('Closes on Tuesday'), null=True))

        # Changing field 'Institution.creation_date'
        db.alter_column('institutions_institution', 'creation_date', self.gf('models.DateTimeField')(_("creation date"), editable=False))

        # Changing field 'Institution.is_invoice_ok'
        db.alter_column('institutions_institution', 'is_invoice_ok', self.gf('models.BooleanField')(_("Invoice")))

        # Changing field 'Institution.sun_break_open'
        db.alter_column('institutions_institution', 'sun_break_open', self.gf('models.TimeField')(_('Break Ends on Sunday'), null=True))

        # Changing field 'Institution.sun_break_close'
        db.alter_column('institutions_institution', 'sun_break_close', self.gf('models.TimeField')(_('Break Starts on Sunday'), null=True))

        # Changing field 'Institution.exceptions_de'
        db.alter_column('institutions_institution', 'exceptions_de', self.gf('ExtendedTextField')(u'Exceptions for working hours', rel=None, unique_for_year=None, unique=False, unique_for_month=None, null=False, primary_key=False, db_column=None, default='', max_length=None, db_tablespace='', unique_for_date=None))

        # Changing field 'Institution.tue_open'
        db.alter_column('institutions_institution', 'tue_open', self.gf('models.TimeField')(_('Opens on Tuesday'), null=True))

        # Changing field 'Institution.description_de'
        db.alter_column('institutions_institution', 'description_de', self.gf('ExtendedTextField')(u'Description', rel=None, unique_for_year=None, unique=False, unique_for_month=None, null=False, primary_key=False, db_column=None, default='', max_length=None, db_tablespace='', unique_for_date=None))

        # Changing field 'Institution.is_non_profit'
        db.alter_column('institutions_institution', 'is_non_profit', self.gf('models.BooleanField')(_("Non profit (business elsewhere)?")))

        # Changing field 'Institution.thu_break_open'
        db.alter_column('institutions_institution', 'thu_break_open', self.gf('models.TimeField')(_('Break Ends on Thursday'), null=True))

        # Changing field 'Institution.wed_open'
        db.alter_column('institutions_institution', 'wed_open', self.gf('models.TimeField')(_('Opens on Wednesday'), null=True))

        # Changing field 'Institution.is_giropay_ok'
        db.alter_column('institutions_institution', 'is_giropay_ok', self.gf('models.BooleanField')(_("Giropay")))

        # Changing field 'Institution.modified_date'
        db.alter_column('institutions_institution', 'modified_date', self.gf('models.DateTimeField')(_("modified date"), null=True, editable=False))

        # Changing field 'Institution.mon_close'
        db.alter_column('institutions_institution', 'mon_close', self.gf('models.TimeField')(_('Closes on Monday'), null=True))

        # Changing field 'Institution.mon_break_close'
        db.alter_column('institutions_institution', 'mon_break_close', self.gf('models.TimeField')(_('Break Starts on Monday'), null=True))

        # Changing field 'Institution.is_transaction_ok'
        db.alter_column('institutions_institution', 'is_transaction_ok', self.gf('models.BooleanField')(_("Bank transfer")))

        # Changing field 'Institution.sat_close'
        db.alter_column('institutions_institution', 'sat_close', self.gf('models.TimeField')(_('Closes on Saturday'), null=True))

        # Changing field 'Institution.sun_open'
        db.alter_column('institutions_institution', 'sun_open', self.gf('models.TimeField')(_('Opens on Sunday'), null=True))

        # Changing field 'Institution.tue_break_close'
        db.alter_column('institutions_institution', 'tue_break_close', self.gf('models.TimeField')(_('Break Starts on Tuesday'), null=True))

        # Changing field 'Institution.vat_id_number'
        db.alter_column('institutions_institution', 'vat_id_number', self.gf('models.CharField')(_("VAT ID"), max_length=100))

        # Changing field 'Institution.title'
        db.alter_column('institutions_institution', 'title', self.gf('models.CharField')(_("Title"), max_length=255))

        # Changing field 'Institution.wed_break_open'
        db.alter_column('institutions_institution', 'wed_break_open', self.gf('models.TimeField')(_('Break Ends on Wednesday'), null=True))

        # Changing field 'Institution.sun_close'
        db.alter_column('institutions_institution', 'sun_close', self.gf('models.TimeField')(_('Closes on Sunday'), null=True))

        # Changing field 'Institution.sat_break_close'
        db.alter_column('institutions_institution', 'sat_break_close', self.gf('models.TimeField')(_('Break Starts on Saturday'), null=True))

        # Changing field 'Institution.fri_break_close'
        db.alter_column('institutions_institution', 'fri_break_close', self.gf('models.TimeField')(_('Break Starts on Friday'), null=True))

        # Changing field 'Institution.is_prepayment_ok'
        db.alter_column('institutions_institution', 'is_prepayment_ok', self.gf('models.BooleanField')(_("Prepayment")))

        # Changing field 'Institution.description'
        db.alter_column('institutions_institution', 'description', self.gf('MultilingualTextField')(_("Description")))

        # Changing field 'Institution.is_wlan_avail'
        db.alter_column('institutions_institution', 'is_wlan_avail', self.gf('models.BooleanField')(_("Is WLAN Internet available?")))

        # Changing field 'Institution.thu_close'
        db.alter_column('institutions_institution', 'thu_close', self.gf('models.TimeField')(_('Closes on Thursday'), null=True))

        # Changing field 'Institution.thu_open'
        db.alter_column('institutions_institution', 'thu_open', self.gf('models.TimeField')(_('Opens on Thursday'), null=True))

        # Changing field 'Institution.description_en'
        db.alter_column('institutions_institution', 'description_en', self.gf('ExtendedTextField')(u'Description', rel=None, unique_for_year=None, unique=False, unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=None, db_tablespace='', unique_for_date=None))

        # Changing field 'Institution.wed_break_close'
        db.alter_column('institutions_institution', 'wed_break_close', self.gf('models.TimeField')(_('Break Starts on Wednesday'), null=True))

        # Changing field 'Institution.is_card_mastercard_ok'
        db.alter_column('institutions_institution', 'is_card_mastercard_ok', self.gf('models.BooleanField')(_("MasterCard")))

        # Changing field 'Institution.legal_form'
        db.alter_column('institutions_institution', 'legal_form_id', self.gf('models.ForeignKey')(orm['structure.Term'], limit_choices_to={'vocabulary__sysname':'basics_legal_form'}, null=True))

        # Changing field 'Institution.is_cash_ok'
        db.alter_column('institutions_institution', 'is_cash_ok', self.gf('models.BooleanField')(_("Cash")))

        # Changing field 'Institution.exceptions_en'
        db.alter_column('institutions_institution', 'exceptions_en', self.gf('ExtendedTextField')(u'Exceptions for working hours', rel=None, unique_for_year=None, unique=False, unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=None, db_tablespace='', unique_for_date=None))

        # Changing field 'Institution.fri_break_open'
        db.alter_column('institutions_institution', 'fri_break_open', self.gf('models.TimeField')(_('Break Ends on Friday'), null=True))

        # Changing field 'Institution.slug'
        db.alter_column('institutions_institution', 'slug', self.gf('models.CharField')(_("Slug"), max_length=255))

        # Changing field 'Institution.mon_open'
        db.alter_column('institutions_institution', 'mon_open', self.gf('models.TimeField')(_('Opens on Monday'), null=True))

        # Changing field 'Institution.is_ec_maestro_ok'
        db.alter_column('institutions_institution', 'is_ec_maestro_ok', self.gf('models.BooleanField')(_("EC Maestro")))

        # Changing field 'Institution.establishment_mm'
        db.alter_column('institutions_institution', 'establishment_mm', self.gf('models.SmallIntegerField')(_("Month of Establishment"), null=True))

        # Changing field 'Institution.sat_open'
        db.alter_column('institutions_institution', 'sat_open', self.gf('models.TimeField')(_('Opens on Saturday'), null=True))

        # Changing field 'Institution.access'
        db.alter_column('institutions_institution', 'access', self.gf('models.CharField')(_("Access"), max_length=255))

        # Changing field 'Institution.is_appointment_based'
        db.alter_column('institutions_institution', 'is_appointment_based', self.gf('models.BooleanField')(_("Visiting by Appointment")))

        # Changing field 'Institution.wed_close'
        db.alter_column('institutions_institution', 'wed_close', self.gf('models.TimeField')(_('Closes on Wednesday'), null=True))

        # Changing field 'Institution.nof_employees'
        db.alter_column('institutions_institution', 'nof_employees', self.gf('models.IntegerField')(_("Number of Employees"), null=True))

        # Changing field 'Institution.status'
        db.alter_column('institutions_institution', 'status_id', self.gf('models.ForeignKey')(orm['structure.Term'], limit_choices_to={'vocabulary__sysname':'basics_object_statuses'}, null=True))

        # Changing field 'Institution.establishment_yyyy'
        db.alter_column('institutions_institution', 'establishment_yyyy', self.gf('models.IntegerField')(_("Year of Establishment"), null=True))

        # Changing field 'Institution.tue_break_open'
        db.alter_column('institutions_institution', 'tue_break_open', self.gf('models.TimeField')(_('Break Ends on Tuesday'), null=True))

        # Changing field 'Institution.exceptions'
        db.alter_column('institutions_institution', 'exceptions', self.gf('MultilingualTextField')(_('Exceptions for working hours')))

        # Changing field 'Institution.is_card_americanexpress_ok'
        db.alter_column('institutions_institution', 'is_card_americanexpress_ok', self.gf('models.BooleanField')(_("American Express")))

        # Changing field 'Institution.mon_break_open'
        db.alter_column('institutions_institution', 'mon_break_open', self.gf('models.TimeField')(_('Break Ends on Monday'), null=True))

        # Changing field 'Institution.is_card_visa_ok'
        db.alter_column('institutions_institution', 'is_card_visa_ok', self.gf('models.BooleanField')(_("Visa")))

        # Changing field 'Institution.title2'
        db.alter_column('institutions_institution', 'title2', self.gf('models.CharField')(_("Title (second line)"), max_length=255))

        # Changing field 'Institution.thu_break_close'
        db.alter_column('institutions_institution', 'thu_break_close', self.gf('models.TimeField')(_('Break Starts on Thursday'), null=True))

        # Changing field 'InstitutionalContact.is_phone2_on_hold'
        db.alter_column('institutions_institutionalcontact', 'is_phone2_on_hold', self.gf('models.BooleanField')(_("On Hold?")))

        # Changing field 'InstitutionalContact.is_im0_default'
        db.alter_column('institutions_institutionalcontact', 'is_im0_default', self.gf('models.BooleanField')(_("Default?")))

        # Changing field 'InstitutionalContact.email0_type'
        db.alter_column('institutions_institutionalcontact', 'email0_type_id', self.gf('models.ForeignKey')(orm['optionset.EmailType'], null=True))

        # Changing field 'InstitutionalContact.is_im2_default'
        db.alter_column('institutions_institutionalcontact', 'is_im2_default', self.gf('models.BooleanField')(_("Default?")))

        # Changing field 'InstitutionalContact.validity_end_mm'
        db.alter_column('institutions_institutionalcontact', 'validity_end_mm', self.gf('models.SmallIntegerField')(_("Till Month"), null=True))

        # Changing field 'InstitutionalContact.is_url0_default'
        db.alter_column('institutions_institutionalcontact', 'is_url0_default', self.gf('models.BooleanField')(_("Default?")))

        # Changing field 'InstitutionalContact.is_primary'
        db.alter_column('institutions_institutionalcontact', 'is_primary', self.gf('models.BooleanField')(_("Primary contact")))

        # Changing field 'InstitutionalContact.is_url2_default'
        db.alter_column('institutions_institutionalcontact', 'is_url2_default', self.gf('models.BooleanField')(_("Default?")))

        # Changing field 'InstitutionalContact.phone1_type'
        db.alter_column('institutions_institutionalcontact', 'phone1_type_id', self.gf('models.ForeignKey')(orm['optionset.PhoneType'], null=True))

        # Changing field 'InstitutionalContact.institution'
        db.alter_column('institutions_institutionalcontact', 'institution_id', self.gf('models.ForeignKey')(orm['institutions.institution']))

        # Changing field 'InstitutionalContact.is_url1_on_hold'
        db.alter_column('institutions_institutionalcontact', 'is_url1_on_hold', self.gf('models.BooleanField')(_("On Hold?")))

        # Changing field 'InstitutionalContact.is_phone0_default'
        db.alter_column('institutions_institutionalcontact', 'is_phone0_default', self.gf('models.BooleanField')(_("Default?")))

        # Changing field 'InstitutionalContact.url1_link'
        db.alter_column('institutions_institutionalcontact', 'url1_link', self.gf('URLField')(_("URL")))

        # Changing field 'InstitutionalContact.validity_start_yyyy'
        db.alter_column('institutions_institutionalcontact', 'validity_start_yyyy', self.gf('models.IntegerField')(_("From Year"), null=True))

        # Changing field 'InstitutionalContact.email1_type'
        db.alter_column('institutions_institutionalcontact', 'email1_type_id', self.gf('models.ForeignKey')(orm['optionset.EmailType'], null=True))

        # Changing field 'InstitutionalContact.phone0_type'
        db.alter_column('institutions_institutionalcontact', 'phone0_type_id', self.gf('models.ForeignKey')(orm['optionset.PhoneType'], null=True))

        # Changing field 'InstitutionalContact.phone2_country'
        db.alter_column('institutions_institutionalcontact', 'phone2_country', self.gf('models.CharField')(_("Country Code"), max_length=4))

        # Changing field 'InstitutionalContact.im1_type'
        db.alter_column('institutions_institutionalcontact', 'im1_type_id', self.gf('models.ForeignKey')(orm['optionset.IMType'], null=True))

        # Changing field 'InstitutionalContact.im2_type'
        db.alter_column('institutions_institutionalcontact', 'im2_type_id', self.gf('models.ForeignKey')(orm['optionset.IMType'], null=True))

        # Changing field 'InstitutionalContact.is_im1_default'
        db.alter_column('institutions_institutionalcontact', 'is_im1_default', self.gf('models.BooleanField')(_("Default?")))

        # Changing field 'InstitutionalContact.is_url2_on_hold'
        db.alter_column('institutions_institutionalcontact', 'is_url2_on_hold', self.gf('models.BooleanField')(_("On Hold?")))

        # Changing field 'InstitutionalContact.is_phone2_default'
        db.alter_column('institutions_institutionalcontact', 'is_phone2_default', self.gf('models.BooleanField')(_("Default?")))

        # Changing field 'InstitutionalContact.phone1_country'
        db.alter_column('institutions_institutionalcontact', 'phone1_country', self.gf('models.CharField')(_("Country Code"), max_length=4))

        # Changing field 'InstitutionalContact.im0_type'
        db.alter_column('institutions_institutionalcontact', 'im0_type_id', self.gf('models.ForeignKey')(orm['optionset.IMType'], null=True))

        # Changing field 'InstitutionalContact.url0_type'
        db.alter_column('institutions_institutionalcontact', 'url0_type_id', self.gf('models.ForeignKey')(orm['optionset.URLType'], null=True))

        # Changing field 'InstitutionalContact.is_phone0_on_hold'
        db.alter_column('institutions_institutionalcontact', 'is_phone0_on_hold', self.gf('models.BooleanField')(_("On Hold?")))

        # Changing field 'InstitutionalContact.validity_start_mm'
        db.alter_column('institutions_institutionalcontact', 'validity_start_mm', self.gf('models.SmallIntegerField')(_("From Month"), null=True))

        # Changing field 'InstitutionalContact.is_email1_default'
        db.alter_column('institutions_institutionalcontact', 'is_email1_default', self.gf('models.BooleanField')(_("Default?")))

        # Changing field 'InstitutionalContact.email2_type'
        db.alter_column('institutions_institutionalcontact', 'email2_type_id', self.gf('models.ForeignKey')(orm['optionset.EmailType'], null=True))

        # Changing field 'InstitutionalContact.validity_start_dd'
        db.alter_column('institutions_institutionalcontact', 'validity_start_dd', self.gf('models.SmallIntegerField')(_("From Day"), null=True))

        # Changing field 'InstitutionalContact.is_email0_on_hold'
        db.alter_column('institutions_institutionalcontact', 'is_email0_on_hold', self.gf('models.BooleanField')(_("On Hold?")))

        # Changing field 'InstitutionalContact.is_im2_on_hold'
        db.alter_column('institutions_institutionalcontact', 'is_im2_on_hold', self.gf('models.BooleanField')(_("On Hold?")))

        # Changing field 'InstitutionalContact.is_email2_default'
        db.alter_column('institutions_institutionalcontact', 'is_email2_default', self.gf('models.BooleanField')(_("Default?")))

        # Changing field 'InstitutionalContact.email0_address'
        db.alter_column('institutions_institutionalcontact', 'email0_address', self.gf('models.CharField')(_("Email Address"), max_length=255))

        # Changing field 'InstitutionalContact.url2_type'
        db.alter_column('institutions_institutionalcontact', 'url2_type_id', self.gf('models.ForeignKey')(orm['optionset.URLType'], null=True))

        # Changing field 'InstitutionalContact.phone0_area'
        db.alter_column('institutions_institutionalcontact', 'phone0_area', self.gf('models.CharField')(_("Area Code"), max_length=5))

        # Changing field 'InstitutionalContact.im1_address'
        db.alter_column('institutions_institutionalcontact', 'im1_address', self.gf('models.CharField')(_("Instant Messenger"), max_length=255))

        # Changing field 'InstitutionalContact.postal_address'
        db.alter_column('institutions_institutionalcontact', 'postal_address_id', self.gf('models.ForeignKey')(orm['location.Address'], null=True))

        # Changing field 'InstitutionalContact.is_email2_on_hold'
        db.alter_column('institutions_institutionalcontact', 'is_email2_on_hold', self.gf('models.BooleanField')(_("On Hold?")))

        # Changing field 'InstitutionalContact.phone0_country'
        db.alter_column('institutions_institutionalcontact', 'phone0_country', self.gf('models.CharField')(_("Country Code"), max_length=4))

        # Changing field 'InstitutionalContact.is_billing_address'
        db.alter_column('institutions_institutionalcontact', 'is_billing_address', self.gf('models.BooleanField')(_("Use this address for billing")))

        # Changing field 'InstitutionalContact.im2_address'
        db.alter_column('institutions_institutionalcontact', 'im2_address', self.gf('models.CharField')(_("Instant Messenger"), max_length=255))

        # Changing field 'InstitutionalContact.location_title'
        db.alter_column('institutions_institutionalcontact', 'location_title', self.gf('models.CharField')(_("Location title"), max_length=255))

        # Changing field 'InstitutionalContact.validity_end_yyyy'
        db.alter_column('institutions_institutionalcontact', 'validity_end_yyyy', self.gf('models.IntegerField')(_("Till Year"), null=True))

        # Changing field 'InstitutionalContact.im0_address'
        db.alter_column('institutions_institutionalcontact', 'im0_address', self.gf('models.CharField')(_("Instant Messenger"), max_length=255))

        # Changing field 'InstitutionalContact.email1_address'
        db.alter_column('institutions_institutionalcontact', 'email1_address', self.gf('models.CharField')(_("Email Address"), max_length=255))

        # Changing field 'InstitutionalContact.location_type'
        db.alter_column('institutions_institutionalcontact', 'location_type_id', self.gf('models.ForeignKey')(orm['optionset.InstitutionalLocationType']))

        # Changing field 'InstitutionalContact.url1_type'
        db.alter_column('institutions_institutionalcontact', 'url1_type_id', self.gf('models.ForeignKey')(orm['optionset.URLType'], null=True))

        # Changing field 'InstitutionalContact.email2_address'
        db.alter_column('institutions_institutionalcontact', 'email2_address', self.gf('models.CharField')(_("Email Address"), max_length=255))

        # Changing field 'InstitutionalContact.is_email0_default'
        db.alter_column('institutions_institutionalcontact', 'is_email0_default', self.gf('models.BooleanField')(_("Default?")))

        # Changing field 'InstitutionalContact.is_phone1_on_hold'
        db.alter_column('institutions_institutionalcontact', 'is_phone1_on_hold', self.gf('models.BooleanField')(_("On Hold?")))

        # Changing field 'InstitutionalContact.validity_end_dd'
        db.alter_column('institutions_institutionalcontact', 'validity_end_dd', self.gf('models.SmallIntegerField')(_("Till Day"), null=True))

        # Changing field 'InstitutionalContact.phone2_type'
        db.alter_column('institutions_institutionalcontact', 'phone2_type_id', self.gf('models.ForeignKey')(orm['optionset.PhoneType'], null=True))

        # Changing field 'InstitutionalContact.is_url1_default'
        db.alter_column('institutions_institutionalcontact', 'is_url1_default', self.gf('models.BooleanField')(_("Default?")))

        # Changing field 'InstitutionalContact.url2_link'
        db.alter_column('institutions_institutionalcontact', 'url2_link', self.gf('URLField')(_("URL")))

        # Changing field 'InstitutionalContact.phone0_number'
        db.alter_column('institutions_institutionalcontact', 'phone0_number', self.gf('models.CharField')(_("Subscriber Number and Extension"), max_length=15))

        # Changing field 'InstitutionalContact.is_email1_on_hold'
        db.alter_column('institutions_institutionalcontact', 'is_email1_on_hold', self.gf('models.BooleanField')(_("On Hold?")))

        # Changing field 'InstitutionalContact.is_im0_on_hold'
        db.alter_column('institutions_institutionalcontact', 'is_im0_on_hold', self.gf('models.BooleanField')(_("On Hold?")))

        # Changing field 'InstitutionalContact.phone1_number'
        db.alter_column('institutions_institutionalcontact', 'phone1_number', self.gf('models.CharField')(_("Subscriber Number and Extension"), max_length=15))

        # Changing field 'InstitutionalContact.is_shipping_address'
        db.alter_column('institutions_institutionalcontact', 'is_shipping_address', self.gf('models.BooleanField')(_("Use this address for shipping")))

        # Changing field 'InstitutionalContact.phone1_area'
        db.alter_column('institutions_institutionalcontact', 'phone1_area', self.gf('models.CharField')(_("Area Code"), max_length=5))

        # Changing field 'InstitutionalContact.is_im1_on_hold'
        db.alter_column('institutions_institutionalcontact', 'is_im1_on_hold', self.gf('models.BooleanField')(_("On Hold?")))

        # Changing field 'InstitutionalContact.is_url0_on_hold'
        db.alter_column('institutions_institutionalcontact', 'is_url0_on_hold', self.gf('models.BooleanField')(_("On Hold?")))

        # Changing field 'InstitutionalContact.phone2_area'
        db.alter_column('institutions_institutionalcontact', 'phone2_area', self.gf('models.CharField')(_("Area Code"), max_length=5))

        # Changing field 'InstitutionalContact.phone2_number'
        db.alter_column('institutions_institutionalcontact', 'phone2_number', self.gf('models.CharField')(_("Subscriber Number and Extension"), max_length=15))

        # Changing field 'InstitutionalContact.is_temporary'
        db.alter_column('institutions_institutionalcontact', 'is_temporary', self.gf('models.BooleanField')(_("Temporary")))

        # Changing field 'InstitutionalContact.is_phone1_default'
        db.alter_column('institutions_institutionalcontact', 'is_phone1_default', self.gf('models.BooleanField')(_("Default?")))

        # Changing field 'InstitutionalContact.url0_link'
        db.alter_column('institutions_institutionalcontact', 'url0_link', self.gf('URLField')(_("URL")))
    
    
    models = {
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('app_label', 'name')", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'i18n.country': {
            'Meta': {'object_name': 'Country'},
            'adm_area': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'iso2_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2', 'primary_key': 'True'}),
            'iso3_code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '56'}),
            'name_de': ('django.db.models.fields.CharField', [], {'max_length': '56', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'sort_order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '20'}),
            'territory_of': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'})
        },
        'institutions.institution': {
            'Meta': {'ordering': "('title', 'title2')", 'object_name': 'Institution'},
            'access': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'context_categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['structure.ContextCategory']", 'symmetrical': 'False', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creative_sectors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'creative_sector_institutions'", 'blank': 'True', 'to': "orm['structure.Term']"}),
            'description': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'description_de': ('base_libs.models.fields.ExtendedTextField', ["u'Beschreibung'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('base_libs.models.fields.ExtendedTextField', ["u'Beschreibung'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'establishment_mm': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'establishment_yyyy': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exceptions': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'exceptions_de': ('base_libs.models.fields.ExtendedTextField', ["u'Sonstige \\xd6ffnungszeiten'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'exceptions_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'exceptions_en': ('base_libs.models.fields.ExtendedTextField', ["u'Sonstige \\xd6ffnungszeiten'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'exceptions_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'exceptions_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'fri_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'fri_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'fri_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'fri_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'directory': "'/institutions/'", 'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']", 'blank': 'True'}),
            'institution_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['structure.Term']", 'symmetrical': 'False'}),
            'is_appointment_based': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_card_americanexpress_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_card_mastercard_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_card_visa_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_cash_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_ec_maestro_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_giropay_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_invoice_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_non_profit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_on_delivery_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_parking_avail': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_paypal_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_prepayment_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_transaction_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_wlan_avail': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'legal_form': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'legal_form_institution'", 'null': 'True', 'to': "orm['structure.Term']"}),
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
            'status': ('django.db.models.fields.related.ForeignKey', [], {'default': '87L', 'related_name': "'status_institution_set'", 'null': 'True', 'blank': 'True', 'to': "orm['structure.Term']"}),
            'status_tmp': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
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
        'institutions.institutionalcontact': {
            'Meta': {'ordering': "['-is_primary']", 'object_name': 'InstitutionalContact'},
            'email0_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'email0_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'institutional_contacts0'", 'null': 'True', 'to': "orm['optionset.EmailType']"}),
            'email1_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'email1_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'institutional_contacts1'", 'null': 'True', 'to': "orm['optionset.EmailType']"}),
            'email2_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'email2_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'institutional_contacts2'", 'null': 'True', 'to': "orm['optionset.EmailType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'im0_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'im0_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'institutional_contacts0'", 'null': 'True', 'to': "orm['optionset.IMType']"}),
            'im1_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'im1_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'institutional_contacts1'", 'null': 'True', 'to': "orm['optionset.IMType']"}),
            'im2_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'im2_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'institutional_contacts2'", 'null': 'True', 'to': "orm['optionset.IMType']"}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['institutions.Institution']"}),
            'is_billing_address': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_email0_default': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_email0_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_email1_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_email1_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_email2_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_email2_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_im0_default': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_im0_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_im1_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_im1_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_im2_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_im2_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_phone0_default': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_phone0_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_phone1_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_phone1_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_phone2_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_phone2_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_primary': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_shipping_address': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_temporary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_url0_default': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_url0_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_url1_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_url1_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_url2_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_url2_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'location_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '1L', 'to': "orm['optionset.InstitutionalLocationType']"}),
            'phone0_area': ('django.db.models.fields.CharField', [], {'default': "'30'", 'max_length': '5', 'blank': 'True'}),
            'phone0_country': ('django.db.models.fields.CharField', [], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'phone0_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'phone0_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '1L', 'related_name': "'institutional_contacts0'", 'null': 'True', 'blank': 'True', 'to': "orm['optionset.PhoneType']"}),
            'phone1_area': ('django.db.models.fields.CharField', [], {'default': "'30'", 'max_length': '5', 'blank': 'True'}),
            'phone1_country': ('django.db.models.fields.CharField', [], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'phone1_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'phone1_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '2L', 'related_name': "'institutional_contacts1'", 'null': 'True', 'blank': 'True', 'to': "orm['optionset.PhoneType']"}),
            'phone2_area': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'phone2_country': ('django.db.models.fields.CharField', [], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'phone2_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'phone2_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '3L', 'related_name': "'institutional_contacts2'", 'null': 'True', 'blank': 'True', 'to': "orm['optionset.PhoneType']"}),
            'postal_address': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'institutional_address'", 'null': 'True', 'to': "orm['location.Address']"}),
            'url0_link': ('base_libs.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'url0_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'institutional_contacts0'", 'null': 'True', 'to': "orm['optionset.URLType']"}),
            'url1_link': ('base_libs.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'url1_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'institutional_contacts1'", 'null': 'True', 'to': "orm['optionset.URLType']"}),
            'url2_link': ('base_libs.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'url2_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'institutional_contacts2'", 'null': 'True', 'to': "orm['optionset.URLType']"}),
            'validity_end_dd': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'validity_end_mm': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'validity_end_yyyy': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'validity_start_dd': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'validity_start_mm': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'validity_start_yyyy': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
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
        'optionset.emailtype': {
            'Meta': {'ordering': "['sort_order', 'title']", 'object_name': 'EmailType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        'optionset.imtype': {
            'Meta': {'ordering': "['sort_order', 'title']", 'object_name': 'IMType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        'optionset.institutionallocationtype': {
            'Meta': {'ordering': "['sort_order', 'title']", 'object_name': 'InstitutionalLocationType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        'optionset.phonetype': {
            'Meta': {'ordering': "['sort_order', 'title']", 'object_name': 'PhoneType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'vcard_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'optionset.urltype': {
            'Meta': {'ordering': "['sort_order', 'title']", 'object_name': 'URLType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
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
        'structure.contextcategory': {
            'Meta': {'ordering': "['path', 'sort_order']", 'object_name': 'ContextCategory'},
            'body': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'body_de': ('base_libs.models.fields.ExtendedTextField', ["u'Inhalt'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'body_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'body_en': ('base_libs.models.fields.ExtendedTextField', ["u'Inhalt'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'body_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'body_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'creative_sectors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['structure.Term']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']", 'blank': 'True'}),
            'is_applied4document': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_applied4event': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_applied4institution': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_applied4person': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_applied4persongroup': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child_set'", 'null': 'True', 'to': "orm['structure.ContextCategory']"}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '8192', 'null': 'True'}),
            'path_search': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'sysname': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        'structure.term': {
            'Meta': {'ordering': "['path', 'sort_order']", 'object_name': 'Term'},
            'body': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'body_de': ('base_libs.models.fields.ExtendedTextField', ["u'Inhalt'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'body_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'body_en': ('base_libs.models.fields.ExtendedTextField', ["u'Inhalt'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'body_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'body_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']", 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child_set'", 'null': 'True', 'to': "orm['structure.Term']"}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '8192', 'null': 'True'}),
            'path_search': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'sysname': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'vocabulary': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structure.Vocabulary']"})
        },
        'structure.vocabulary': {
            'Meta': {'object_name': 'Vocabulary'},
            'body': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'body_de': ('base_libs.models.fields.ExtendedTextField', ["u'Inhalt'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'body_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'body_en': ('base_libs.models.fields.ExtendedTextField', ["u'Inhalt'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'body_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'body_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'hierarchy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']", 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'sysname': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['institutions']
