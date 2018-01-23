# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'Museum.admission_price'
        db.add_column('museums_museum', 'admission_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True), keep_default=False)

        # Adding field 'Museum.admission_price_info'
        db.add_column('museums_museum', 'admission_price_info', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True), keep_default=False)

        # Adding field 'Museum.reduced_price'
        db.add_column('museums_museum', 'reduced_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True), keep_default=False)

        # Adding field 'Museum.reduced_price_info'
        db.add_column('museums_museum', 'reduced_price_info', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True), keep_default=False)

        # Adding field 'Museum.arrangements_for_children'
        db.add_column('museums_museum', 'arrangements_for_children', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True), keep_default=False)

        # Adding field 'Museum.free_entrance_for'
        db.add_column('museums_museum', 'free_entrance_for', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True), keep_default=False)

        # Adding field 'Museum.family_ticket'
        db.add_column('museums_museum', 'family_ticket', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True), keep_default=False)

        # Adding field 'Museum.group_ticket'
        db.add_column('museums_museum', 'group_ticket', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True), keep_default=False)

        # Adding field 'Museum.free_entrance_times'
        db.add_column('museums_museum', 'free_entrance_times', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True), keep_default=False)

        # Adding field 'Museum.yearly_ticket'
        db.add_column('museums_museum', 'yearly_ticket', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True), keep_default=False)

        # Adding field 'Museum.other_tickets'
        db.add_column('museums_museum', 'other_tickets', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True), keep_default=False)

        # Adding field 'Museum.member_of_museumspass'
        db.add_column('museums_museum', 'member_of_museumspass', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Museum.yearly_ticket_de'
        db.add_column('museums_museum', 'yearly_ticket_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Yearly ticket', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False), keep_default=False)

        # Adding field 'Museum.yearly_ticket_de_markup_type'
        db.add_column('museums_museum', 'yearly_ticket_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Museum.yearly_ticket_en'
        db.add_column('museums_museum', 'yearly_ticket_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Yearly ticket', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False), keep_default=False)

        # Adding field 'Museum.yearly_ticket_en_markup_type'
        db.add_column('museums_museum', 'yearly_ticket_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Museum.yearly_ticket_markup_type'
        db.add_column('museums_museum', 'yearly_ticket_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Museum.reduced_price_info_de'
        db.add_column('museums_museum', 'reduced_price_info_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Reduced admission price info', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False), keep_default=False)

        # Adding field 'Museum.reduced_price_info_de_markup_type'
        db.add_column('museums_museum', 'reduced_price_info_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Museum.reduced_price_info_en'
        db.add_column('museums_museum', 'reduced_price_info_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Reduced admission price info', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False), keep_default=False)

        # Adding field 'Museum.reduced_price_info_en_markup_type'
        db.add_column('museums_museum', 'reduced_price_info_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Museum.reduced_price_info_markup_type'
        db.add_column('museums_museum', 'reduced_price_info_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Museum.group_ticket_de'
        db.add_column('museums_museum', 'group_ticket_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Group ticket', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False), keep_default=False)

        # Adding field 'Museum.group_ticket_de_markup_type'
        db.add_column('museums_museum', 'group_ticket_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Museum.group_ticket_en'
        db.add_column('museums_museum', 'group_ticket_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Group ticket', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False), keep_default=False)

        # Adding field 'Museum.group_ticket_en_markup_type'
        db.add_column('museums_museum', 'group_ticket_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Museum.group_ticket_markup_type'
        db.add_column('museums_museum', 'group_ticket_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Museum.arrangements_for_children_de'
        db.add_column('museums_museum', 'arrangements_for_children_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Admission arrangements for children and youth', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False), keep_default=False)

        # Adding field 'Museum.arrangements_for_children_de_markup_type'
        db.add_column('museums_museum', 'arrangements_for_children_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Museum.arrangements_for_children_en'
        db.add_column('museums_museum', 'arrangements_for_children_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Admission arrangements for children and youth', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False), keep_default=False)

        # Adding field 'Museum.arrangements_for_children_en_markup_type'
        db.add_column('museums_museum', 'arrangements_for_children_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Museum.arrangements_for_children_markup_type'
        db.add_column('museums_museum', 'arrangements_for_children_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Museum.free_entrance_times_de'
        db.add_column('museums_museum', 'free_entrance_times_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Yearly ticket', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False), keep_default=False)

        # Adding field 'Museum.free_entrance_times_de_markup_type'
        db.add_column('museums_museum', 'free_entrance_times_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Museum.free_entrance_times_en'
        db.add_column('museums_museum', 'free_entrance_times_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Free entrance times', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False), keep_default=False)

        # Adding field 'Museum.free_entrance_times_en_markup_type'
        db.add_column('museums_museum', 'free_entrance_times_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Museum.free_entrance_times_markup_type'
        db.add_column('museums_museum', 'free_entrance_times_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Museum.free_entrance_for_de'
        db.add_column('museums_museum', 'free_entrance_for_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Free entrance for', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False), keep_default=False)

        # Adding field 'Museum.free_entrance_for_de_markup_type'
        db.add_column('museums_museum', 'free_entrance_for_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Museum.free_entrance_for_en'
        db.add_column('museums_museum', 'free_entrance_for_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Free entrance for', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False), keep_default=False)

        # Adding field 'Museum.free_entrance_for_en_markup_type'
        db.add_column('museums_museum', 'free_entrance_for_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Museum.free_entrance_for_markup_type'
        db.add_column('museums_museum', 'free_entrance_for_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Museum.family_ticket_de'
        db.add_column('museums_museum', 'family_ticket_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Family ticket', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False), keep_default=False)

        # Adding field 'Museum.family_ticket_de_markup_type'
        db.add_column('museums_museum', 'family_ticket_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Museum.family_ticket_en'
        db.add_column('museums_museum', 'family_ticket_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Family ticket', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False), keep_default=False)

        # Adding field 'Museum.family_ticket_en_markup_type'
        db.add_column('museums_museum', 'family_ticket_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Museum.family_ticket_markup_type'
        db.add_column('museums_museum', 'family_ticket_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Museum.other_tickets_de'
        db.add_column('museums_museum', 'other_tickets_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Other tickets', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False), keep_default=False)

        # Adding field 'Museum.other_tickets_de_markup_type'
        db.add_column('museums_museum', 'other_tickets_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Museum.other_tickets_en'
        db.add_column('museums_museum', 'other_tickets_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Other tickets', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False), keep_default=False)

        # Adding field 'Museum.other_tickets_en_markup_type'
        db.add_column('museums_museum', 'other_tickets_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Museum.other_tickets_markup_type'
        db.add_column('museums_museum', 'other_tickets_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Museum.admission_price_info_de'
        db.add_column('museums_museum', 'admission_price_info_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Admission price info', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False), keep_default=False)

        # Adding field 'Museum.admission_price_info_de_markup_type'
        db.add_column('museums_museum', 'admission_price_info_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Museum.admission_price_info_en'
        db.add_column('museums_museum', 'admission_price_info_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Admission price info', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False), keep_default=False)

        # Adding field 'Museum.admission_price_info_en_markup_type'
        db.add_column('museums_museum', 'admission_price_info_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Museum.admission_price_info_markup_type'
        db.add_column('museums_museum', 'admission_price_info_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Deleting field 'Museum.admission_price'
        db.delete_column('museums_museum', 'admission_price')

        # Deleting field 'Museum.admission_price_info'
        db.delete_column('museums_museum', 'admission_price_info')

        # Deleting field 'Museum.reduced_price'
        db.delete_column('museums_museum', 'reduced_price')

        # Deleting field 'Museum.reduced_price_info'
        db.delete_column('museums_museum', 'reduced_price_info')

        # Deleting field 'Museum.arrangements_for_children'
        db.delete_column('museums_museum', 'arrangements_for_children')

        # Deleting field 'Museum.free_entrance_for'
        db.delete_column('museums_museum', 'free_entrance_for')

        # Deleting field 'Museum.family_ticket'
        db.delete_column('museums_museum', 'family_ticket')

        # Deleting field 'Museum.group_ticket'
        db.delete_column('museums_museum', 'group_ticket')

        # Deleting field 'Museum.free_entrance_times'
        db.delete_column('museums_museum', 'free_entrance_times')

        # Deleting field 'Museum.yearly_ticket'
        db.delete_column('museums_museum', 'yearly_ticket')

        # Deleting field 'Museum.other_tickets'
        db.delete_column('museums_museum', 'other_tickets')

        # Deleting field 'Museum.member_of_museumspass'
        db.delete_column('museums_museum', 'member_of_museumspass')

        # Deleting field 'Museum.yearly_ticket_de'
        db.delete_column('museums_museum', 'yearly_ticket_de')

        # Deleting field 'Museum.yearly_ticket_de_markup_type'
        db.delete_column('museums_museum', 'yearly_ticket_de_markup_type')

        # Deleting field 'Museum.yearly_ticket_en'
        db.delete_column('museums_museum', 'yearly_ticket_en')

        # Deleting field 'Museum.yearly_ticket_en_markup_type'
        db.delete_column('museums_museum', 'yearly_ticket_en_markup_type')

        # Deleting field 'Museum.yearly_ticket_markup_type'
        db.delete_column('museums_museum', 'yearly_ticket_markup_type')

        # Deleting field 'Museum.reduced_price_info_de'
        db.delete_column('museums_museum', 'reduced_price_info_de')

        # Deleting field 'Museum.reduced_price_info_de_markup_type'
        db.delete_column('museums_museum', 'reduced_price_info_de_markup_type')

        # Deleting field 'Museum.reduced_price_info_en'
        db.delete_column('museums_museum', 'reduced_price_info_en')

        # Deleting field 'Museum.reduced_price_info_en_markup_type'
        db.delete_column('museums_museum', 'reduced_price_info_en_markup_type')

        # Deleting field 'Museum.reduced_price_info_markup_type'
        db.delete_column('museums_museum', 'reduced_price_info_markup_type')

        # Deleting field 'Museum.group_ticket_de'
        db.delete_column('museums_museum', 'group_ticket_de')

        # Deleting field 'Museum.group_ticket_de_markup_type'
        db.delete_column('museums_museum', 'group_ticket_de_markup_type')

        # Deleting field 'Museum.group_ticket_en'
        db.delete_column('museums_museum', 'group_ticket_en')

        # Deleting field 'Museum.group_ticket_en_markup_type'
        db.delete_column('museums_museum', 'group_ticket_en_markup_type')

        # Deleting field 'Museum.group_ticket_markup_type'
        db.delete_column('museums_museum', 'group_ticket_markup_type')

        # Deleting field 'Museum.arrangements_for_children_de'
        db.delete_column('museums_museum', 'arrangements_for_children_de')

        # Deleting field 'Museum.arrangements_for_children_de_markup_type'
        db.delete_column('museums_museum', 'arrangements_for_children_de_markup_type')

        # Deleting field 'Museum.arrangements_for_children_en'
        db.delete_column('museums_museum', 'arrangements_for_children_en')

        # Deleting field 'Museum.arrangements_for_children_en_markup_type'
        db.delete_column('museums_museum', 'arrangements_for_children_en_markup_type')

        # Deleting field 'Museum.arrangements_for_children_markup_type'
        db.delete_column('museums_museum', 'arrangements_for_children_markup_type')

        # Deleting field 'Museum.free_entrance_times_de'
        db.delete_column('museums_museum', 'free_entrance_times_de')

        # Deleting field 'Museum.free_entrance_times_de_markup_type'
        db.delete_column('museums_museum', 'free_entrance_times_de_markup_type')

        # Deleting field 'Museum.free_entrance_times_en'
        db.delete_column('museums_museum', 'free_entrance_times_en')

        # Deleting field 'Museum.free_entrance_times_en_markup_type'
        db.delete_column('museums_museum', 'free_entrance_times_en_markup_type')

        # Deleting field 'Museum.free_entrance_times_markup_type'
        db.delete_column('museums_museum', 'free_entrance_times_markup_type')

        # Deleting field 'Museum.free_entrance_for_de'
        db.delete_column('museums_museum', 'free_entrance_for_de')

        # Deleting field 'Museum.free_entrance_for_de_markup_type'
        db.delete_column('museums_museum', 'free_entrance_for_de_markup_type')

        # Deleting field 'Museum.free_entrance_for_en'
        db.delete_column('museums_museum', 'free_entrance_for_en')

        # Deleting field 'Museum.free_entrance_for_en_markup_type'
        db.delete_column('museums_museum', 'free_entrance_for_en_markup_type')

        # Deleting field 'Museum.free_entrance_for_markup_type'
        db.delete_column('museums_museum', 'free_entrance_for_markup_type')

        # Deleting field 'Museum.family_ticket_de'
        db.delete_column('museums_museum', 'family_ticket_de')

        # Deleting field 'Museum.family_ticket_de_markup_type'
        db.delete_column('museums_museum', 'family_ticket_de_markup_type')

        # Deleting field 'Museum.family_ticket_en'
        db.delete_column('museums_museum', 'family_ticket_en')

        # Deleting field 'Museum.family_ticket_en_markup_type'
        db.delete_column('museums_museum', 'family_ticket_en_markup_type')

        # Deleting field 'Museum.family_ticket_markup_type'
        db.delete_column('museums_museum', 'family_ticket_markup_type')

        # Deleting field 'Museum.other_tickets_de'
        db.delete_column('museums_museum', 'other_tickets_de')

        # Deleting field 'Museum.other_tickets_de_markup_type'
        db.delete_column('museums_museum', 'other_tickets_de_markup_type')

        # Deleting field 'Museum.other_tickets_en'
        db.delete_column('museums_museum', 'other_tickets_en')

        # Deleting field 'Museum.other_tickets_en_markup_type'
        db.delete_column('museums_museum', 'other_tickets_en_markup_type')

        # Deleting field 'Museum.other_tickets_markup_type'
        db.delete_column('museums_museum', 'other_tickets_markup_type')

        # Deleting field 'Museum.admission_price_info_de'
        db.delete_column('museums_museum', 'admission_price_info_de')

        # Deleting field 'Museum.admission_price_info_de_markup_type'
        db.delete_column('museums_museum', 'admission_price_info_de_markup_type')

        # Deleting field 'Museum.admission_price_info_en'
        db.delete_column('museums_museum', 'admission_price_info_en')

        # Deleting field 'Museum.admission_price_info_en_markup_type'
        db.delete_column('museums_museum', 'admission_price_info_en_markup_type')

        # Deleting field 'Museum.admission_price_info_markup_type'
        db.delete_column('museums_museum', 'admission_price_info_markup_type')
    
    
    models = {
        'museums.museum': {
            'Meta': {'ordering': "['title']", 'object_name': 'Museum'},
            'admission_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'admission_price_info': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'admission_price_info_de': ('base_libs.models.fields.ExtendedTextField', ["u'Admission price info'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'admission_price_info_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'admission_price_info_en': ('base_libs.models.fields.ExtendedTextField', ["u'Admission price info'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'admission_price_info_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'admission_price_info_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'arrangements_for_children': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'arrangements_for_children_de': ('base_libs.models.fields.ExtendedTextField', ["u'Admission arrangements for children and youth'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'arrangements_for_children_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'arrangements_for_children_en': ('base_libs.models.fields.ExtendedTextField', ["u'Admission arrangements for children and youth'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'arrangements_for_children_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'arrangements_for_children_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['museums.MuseumCategory']", 'symmetrical': 'False'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "'Berlin'", 'max_length': '255'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'de'", 'max_length': '255'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'description_de': ('base_libs.models.fields.ExtendedTextField', ["u'Beschreibung'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('base_libs.models.fields.ExtendedTextField', ["u'Beschreibung'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'blank': 'True'}),
            'family_ticket': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'family_ticket_de': ('base_libs.models.fields.ExtendedTextField', ["u'Family ticket'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'family_ticket_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'family_ticket_en': ('base_libs.models.fields.ExtendedTextField', ["u'Family ticket'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'family_ticket_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'family_ticket_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'free_entrance': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'free_entrance_for': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'free_entrance_for_de': ('base_libs.models.fields.ExtendedTextField', ["u'Free entrance for'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'free_entrance_for_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'free_entrance_for_en': ('base_libs.models.fields.ExtendedTextField', ["u'Free entrance for'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'free_entrance_for_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'free_entrance_for_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'free_entrance_times': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'free_entrance_times_de': ('base_libs.models.fields.ExtendedTextField', ["u'Free entrance times'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'free_entrance_times_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'free_entrance_times_en': ('base_libs.models.fields.ExtendedTextField', ["u'Free entrance times'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'free_entrance_times_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'free_entrance_times_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'group_ticket': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'group_ticket_de': ('base_libs.models.fields.ExtendedTextField', ["u'Group ticket'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'group_ticket_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'group_ticket_en': ('base_libs.models.fields.ExtendedTextField', ["u'Group ticket'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'group_ticket_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'group_ticket_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'directory': "'museums/'", 'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']", 'blank': 'True'}),
            'image_caption': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_caption_de': ('base_libs.models.fields.ExtendedTextField', ["u'Bildbeschreibung'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': '255', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'image_caption_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'image_caption_en': ('base_libs.models.fields.ExtendedTextField', ["u'Bildbeschreibung'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': '255', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'image_caption_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'image_caption_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'member_of_museumspass': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'open_on_mondays': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'other_tickets': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'other_tickets_de': ('base_libs.models.fields.ExtendedTextField', ["u'Other tickets'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'other_tickets_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'other_tickets_en': ('base_libs.models.fields.ExtendedTextField', ["u'Other tickets'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'other_tickets_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'other_tickets_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'press_text': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'press_text_de': ('base_libs.models.fields.ExtendedTextField', ["u'Press text'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'press_text_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'press_text_en': ('base_libs.models.fields.ExtendedTextField', ["u'Press text'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'press_text_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'press_text_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'reduced_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'reduced_price_info': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'reduced_price_info_de': ('base_libs.models.fields.ExtendedTextField', ["u'Reduced admission price info'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'reduced_price_info_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'reduced_price_info_en': ('base_libs.models.fields.ExtendedTextField', ["u'Reduced admission price info'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'reduced_price_info_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'reduced_price_info_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['museums.MuseumService']", 'symmetrical': 'False', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'draft'", 'max_length': '20', 'blank': 'True'}),
            'street_address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'street_address2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'subtitle': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subtitle_de': ('django.db.models.fields.CharField', ["u'Subtitle'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'subtitle_en': ('django.db.models.fields.CharField', ["u'Subtitle'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'tags': ('tagging_autocomplete.models.TagAutocompleteField', [], {'default': "''"}),
            'teaser': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'teaser_de': ('base_libs.models.fields.ExtendedTextField', ["u'Teaser'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'teaser_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'teaser_en': ('base_libs.models.fields.ExtendedTextField', ["u'Teaser'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'teaser_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'teaser_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'website': ('base_libs.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'yearly_ticket': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'yearly_ticket_de': ('base_libs.models.fields.ExtendedTextField', ["u'Yearly ticket'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'yearly_ticket_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'yearly_ticket_en': ('base_libs.models.fields.ExtendedTextField', ["u'Yearly ticket'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'yearly_ticket_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'yearly_ticket_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'})
        },
        'museums.museumcategory': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'MuseumCategory'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '200', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        'museums.museumservice': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'MuseumService'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '200', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['museums']
