# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Deleting field 'Museum.mediation_offer'
        db.delete_column('museums_museum', 'mediation_offer')

        # Deleting field 'Museum.mediation_offer_en_markup_type'
        db.delete_column('museums_museum', 'mediation_offer_en_markup_type')

        # Deleting field 'Museum.mediation_offer_markup_type'
        db.delete_column('museums_museum', 'mediation_offer_markup_type')

        # Deleting field 'Museum.mediation_offer_de_markup_type'
        db.delete_column('museums_museum', 'mediation_offer_de_markup_type')

        # Deleting field 'Museum.mediation_offer_en'
        db.delete_column('museums_museum', 'mediation_offer_en')

        # Deleting field 'Museum.mediation_offer_de'
        db.delete_column('museums_museum', 'mediation_offer_de')

        # Adding field 'Museum.has_audioguide'
        db.add_column('museums_museum', 'has_audioguide', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Museum.has_audioguide_de'
        db.add_column('museums_museum', 'has_audioguide_de', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Museum.has_audioguide_en'
        db.add_column('museums_museum', 'has_audioguide_en', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Museum.has_audioguide_fr'
        db.add_column('museums_museum', 'has_audioguide_fr', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Museum.has_audioguide_it'
        db.add_column('museums_museum', 'has_audioguide_it', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Museum.has_audioguide_sp'
        db.add_column('museums_museum', 'has_audioguide_sp', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Museum.has_audioguide_pl'
        db.add_column('museums_museum', 'has_audioguide_pl', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Museum.has_audioguide_tr'
        db.add_column('museums_museum', 'has_audioguide_tr', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Museum.audioguide_other_languages'
        db.add_column('museums_museum', 'audioguide_other_languages', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True), keep_default=False)

        # Adding field 'Museum.has_audioguide_for_children'
        db.add_column('museums_museum', 'has_audioguide_for_children', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Museum.has_audioguide_for_learning_difficulties'
        db.add_column('museums_museum', 'has_audioguide_for_learning_difficulties', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Adding field 'Museum.mediation_offer'
        db.add_column('museums_museum', 'mediation_offer', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True), keep_default=False)

        # Adding field 'Museum.mediation_offer_en_markup_type'
        db.add_column('museums_museum', 'mediation_offer_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Museum.mediation_offer_markup_type'
        db.add_column('museums_museum', 'mediation_offer_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Museum.mediation_offer_de_markup_type'
        db.add_column('museums_museum', 'mediation_offer_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'Museum.mediation_offer_en'
        db.add_column('museums_museum', 'mediation_offer_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Weitere Vermittlungsangebote', rel=None, unique_for_year=None, blank=True, unique_for_date=None, db_index=False, unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, db_tablespace=''), keep_default=False)

        # Adding field 'Museum.mediation_offer_de'
        db.add_column('museums_museum', 'mediation_offer_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Weitere Vermittlungsangebote', rel=None, unique_for_year=None, blank=True, unique_for_date=None, db_index=False, unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, db_tablespace=''), keep_default=False)

        # Deleting field 'Museum.has_audioguide'
        db.delete_column('museums_museum', 'has_audioguide')

        # Deleting field 'Museum.has_audioguide_de'
        db.delete_column('museums_museum', 'has_audioguide_de')

        # Deleting field 'Museum.has_audioguide_en'
        db.delete_column('museums_museum', 'has_audioguide_en')

        # Deleting field 'Museum.has_audioguide_fr'
        db.delete_column('museums_museum', 'has_audioguide_fr')

        # Deleting field 'Museum.has_audioguide_it'
        db.delete_column('museums_museum', 'has_audioguide_it')

        # Deleting field 'Museum.has_audioguide_sp'
        db.delete_column('museums_museum', 'has_audioguide_sp')

        # Deleting field 'Museum.has_audioguide_pl'
        db.delete_column('museums_museum', 'has_audioguide_pl')

        # Deleting field 'Museum.has_audioguide_tr'
        db.delete_column('museums_museum', 'has_audioguide_tr')

        # Deleting field 'Museum.audioguide_other_languages'
        db.delete_column('museums_museum', 'audioguide_other_languages')

        # Deleting field 'Museum.has_audioguide_for_children'
        db.delete_column('museums_museum', 'has_audioguide_for_children')

        # Deleting field 'Museum.has_audioguide_for_learning_difficulties'
        db.delete_column('museums_museum', 'has_audioguide_for_learning_difficulties')
    
    
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
        'museums.accessibilityoption': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'AccessibilityOption'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'directory': "'accessibility/'", 'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']", 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '200', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        'museums.mediafile': {
            'Meta': {'ordering': "['sort_order', 'creation_date']", 'object_name': 'MediaFile'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'museum': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['museums.Museum']"}),
            'path': ('filebrowser.fields.FileBrowseField', [], {'directory': "'museums/'", 'max_length': '255'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': 'None'})
        },
        'museums.museum': {
            'Meta': {'ordering': "['title']", 'object_name': 'Museum'},
            'accessibility': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'accessibility_de': ('base_libs.models.fields.ExtendedTextField', ["u'Barrierefreiheit'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'accessibility_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'accessibility_en': ('base_libs.models.fields.ExtendedTextField', ["u'Barrierefreiheit'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'accessibility_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'accessibility_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'accessibility_options': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['museums.AccessibilityOption']", 'symmetrical': 'False', 'blank': 'True'}),
            'admission_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'admission_price_info': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'admission_price_info_de': ('base_libs.models.fields.ExtendedTextField', ["u'Preisinformation'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'admission_price_info_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'admission_price_info_en': ('base_libs.models.fields.ExtendedTextField', ["u'Preisinformation'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'admission_price_info_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'admission_price_info_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'audioguide_other_languages': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'categories': ('mptt.fields.TreeManyToManyField', [], {'to': "orm['museums.MuseumCategory']", 'symmetrical': 'False'}),
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
            'facebook': ('base_libs.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'fax_area': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'fax_country': ('django.db.models.fields.CharField', [], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'fax_number': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'free_entrance': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'group_bookings_phone_area': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'group_bookings_phone_country': ('django.db.models.fields.CharField', [], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'group_bookings_phone_number': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'group_ticket': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'group_ticket_de': ('base_libs.models.fields.ExtendedTextField', ["u'Gruppenticket'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'group_ticket_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'group_ticket_en': ('base_libs.models.fields.ExtendedTextField', ["u'Gruppenticket'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'group_ticket_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'group_ticket_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'has_audioguide': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_audioguide_de': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_audioguide_en': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_audioguide_for_children': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_audioguide_for_learning_difficulties': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_audioguide_fr': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_audioguide_it': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_audioguide_pl': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_audioguide_sp': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_audioguide_tr': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'directory': "'museums/'", 'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']", 'blank': 'True'}),
            'image_caption': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_caption_de': ('base_libs.models.fields.ExtendedTextField', ["u'Bildbeschreibung'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': '255', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'image_caption_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'image_caption_en': ('base_libs.models.fields.ExtendedTextField', ["u'Bildbeschreibung'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': '255', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'image_caption_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'image_caption_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'is_for_children': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'member_of_museumspass': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'open_on_mondays': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone_area': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'phone_country': ('django.db.models.fields.CharField', [], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'press_text': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'press_text_de': ('base_libs.models.fields.ExtendedTextField', ["u'Pressetext'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'press_text_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'press_text_en': ('base_libs.models.fields.ExtendedTextField', ["u'Pressetext'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'press_text_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'press_text_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'reduced_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'reduced_price_info': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'reduced_price_info_de': ('base_libs.models.fields.ExtendedTextField', ["u'Erm\\xe4\\xdfigter Eintritt Infotext'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'reduced_price_info_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'reduced_price_info_en': ('base_libs.models.fields.ExtendedTextField', ["u'Erm\\xe4\\xdfigter Eintritt Infotext'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'reduced_price_info_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'reduced_price_info_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'service_archive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'service_cafe': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'service_diaper_changing_table': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'service_library': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'service_phone_area': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'service_phone_country': ('django.db.models.fields.CharField', [], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'service_phone_number': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'service_restaurant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'service_shop': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_family_ticket': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_group_ticket': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_yearly_ticket': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'draft'", 'max_length': '20', 'blank': 'True'}),
            'street_address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'street_address2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'subtitle': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subtitle_de': ('django.db.models.fields.CharField', ["u'Subtitle'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'subtitle_en': ('django.db.models.fields.CharField', ["u'Subtitle'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'tags': ('tagging_autocomplete.models.TagAutocompleteField', [], {'default': "''"}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Name'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Name'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'website': ('base_libs.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'museums.museumcategory': {
            'Meta': {'ordering': "['tree_id', 'lft']", 'object_name': 'MuseumCategory'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'to': "orm['museums.MuseumCategory']", 'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '200', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'museums.season': {
            'Meta': {'ordering': "('start',)", 'object_name': 'Season'},
            'end': ('django.db.models.fields.DateField', [], {}),
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
            'is_appointment_based': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_entry': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'last_entry_de': ('django.db.models.fields.CharField', ["u'Last entry'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'last_entry_en': ('django.db.models.fields.CharField', ["u'Last entry'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'mon_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'mon_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'mon_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'mon_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'museum': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['museums.Museum']"}),
            'sat_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'sat_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'sat_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'sat_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateField', [], {}),
            'sun_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'sun_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'sun_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'sun_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'thu_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'thu_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'thu_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'thu_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Season title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Season title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'tue_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'tue_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'tue_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'tue_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'wed_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'wed_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'wed_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'wed_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'museums.specialopeningtime': {
            'Meta': {'ordering': "('yyyy', 'mm', 'dd')", 'object_name': 'SpecialOpeningTime'},
            'break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'closing': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'day_label': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'day_label_de': ('django.db.models.fields.CharField', ["u'Day label'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'day_label_en': ('django.db.models.fields.CharField', ["u'Day label'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'dd': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'exceptions': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'exceptions_de': ('base_libs.models.fields.ExtendedTextField', ["u'Sonstige \\xd6ffnungszeiten'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'exceptions_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'exceptions_en': ('base_libs.models.fields.ExtendedTextField', ["u'Sonstige \\xd6ffnungszeiten'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'exceptions_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'exceptions_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_regular': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mm': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'museum': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['museums.Museum']"}),
            'opening': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'yyyy': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
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
    
    complete_apps = ['museums']
