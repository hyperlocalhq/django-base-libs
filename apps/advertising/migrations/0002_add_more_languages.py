# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
                # Deleting field 'AdZone.description_markup_type'
        db.delete_column(u'advertising_adzone', 'description_markup_type')

        # Adding field 'AdZone.description_fr'
        db.add_column(u'advertising_adzone', 'description_fr',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'AdZone.description_fr_markup_type'
        db.add_column(u'advertising_adzone', 'description_fr_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'AdZone.description_pl'
        db.add_column(u'advertising_adzone', 'description_pl',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'AdZone.description_pl_markup_type'
        db.add_column(u'advertising_adzone', 'description_pl_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'AdZone.description_tr'
        db.add_column(u'advertising_adzone', 'description_tr',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'AdZone.description_tr_markup_type'
        db.add_column(u'advertising_adzone', 'description_tr_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'AdZone.description_es'
        db.add_column(u'advertising_adzone', 'description_es',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'AdZone.description_es_markup_type'
        db.add_column(u'advertising_adzone', 'description_es_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'AdZone.description_it'
        db.add_column(u'advertising_adzone', 'description_it',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'AdZone.description_it_markup_type'
        db.add_column(u'advertising_adzone', 'description_it_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'AdZone.title_fr'
        db.add_column(u'advertising_adzone', 'title_fr',
                      self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'AdZone.title_pl'
        db.add_column(u'advertising_adzone', 'title_pl',
                      self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'AdZone.title_tr'
        db.add_column(u'advertising_adzone', 'title_tr',
                      self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'AdZone.title_es'
        db.add_column(u'advertising_adzone', 'title_es',
                      self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'AdZone.title_it'
        db.add_column(u'advertising_adzone', 'title_it',
                      self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)


        # Changing field 'AdZone.description_en'
        db.alter_column(u'advertising_adzone', 'description_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, unique=False, db_tablespace=''))

        # Changing field 'AdZone.description_de'
        db.alter_column(u'advertising_adzone', 'description_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, unique=False, db_tablespace=''))
        # Deleting field 'AdCategory.description_markup_type'
        db.delete_column(u'advertising_adcategory', 'description_markup_type')

        # Adding field 'AdCategory.description_fr'
        db.add_column(u'advertising_adcategory', 'description_fr',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'AdCategory.description_fr_markup_type'
        db.add_column(u'advertising_adcategory', 'description_fr_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'AdCategory.description_pl'
        db.add_column(u'advertising_adcategory', 'description_pl',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'AdCategory.description_pl_markup_type'
        db.add_column(u'advertising_adcategory', 'description_pl_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'AdCategory.description_tr'
        db.add_column(u'advertising_adcategory', 'description_tr',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'AdCategory.description_tr_markup_type'
        db.add_column(u'advertising_adcategory', 'description_tr_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'AdCategory.description_es'
        db.add_column(u'advertising_adcategory', 'description_es',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'AdCategory.description_es_markup_type'
        db.add_column(u'advertising_adcategory', 'description_es_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'AdCategory.description_it'
        db.add_column(u'advertising_adcategory', 'description_it',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'AdCategory.description_it_markup_type'
        db.add_column(u'advertising_adcategory', 'description_it_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'AdCategory.title_fr'
        db.add_column(u'advertising_adcategory', 'title_fr',
                      self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'AdCategory.title_pl'
        db.add_column(u'advertising_adcategory', 'title_pl',
                      self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'AdCategory.title_tr'
        db.add_column(u'advertising_adcategory', 'title_tr',
                      self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'AdCategory.title_es'
        db.add_column(u'advertising_adcategory', 'title_es',
                      self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'AdCategory.title_it'
        db.add_column(u'advertising_adcategory', 'title_it',
                      self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)


        # Changing field 'AdCategory.description_en'
        db.alter_column(u'advertising_adcategory', 'description_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, unique=False, db_tablespace=''))

        # Changing field 'AdCategory.description_de'
        db.alter_column(u'advertising_adcategory', 'description_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, unique=False, db_tablespace=''))
    
    
    def backwards(self, orm):
                # Adding field 'AdZone.description_markup_type'
        db.add_column(u'advertising_adzone', 'description_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Deleting field 'AdZone.description_fr'
        db.delete_column(u'advertising_adzone', 'description_fr')

        # Deleting field 'AdZone.description_fr_markup_type'
        db.delete_column(u'advertising_adzone', 'description_fr_markup_type')

        # Deleting field 'AdZone.description_pl'
        db.delete_column(u'advertising_adzone', 'description_pl')

        # Deleting field 'AdZone.description_pl_markup_type'
        db.delete_column(u'advertising_adzone', 'description_pl_markup_type')

        # Deleting field 'AdZone.description_tr'
        db.delete_column(u'advertising_adzone', 'description_tr')

        # Deleting field 'AdZone.description_tr_markup_type'
        db.delete_column(u'advertising_adzone', 'description_tr_markup_type')

        # Deleting field 'AdZone.description_es'
        db.delete_column(u'advertising_adzone', 'description_es')

        # Deleting field 'AdZone.description_es_markup_type'
        db.delete_column(u'advertising_adzone', 'description_es_markup_type')

        # Deleting field 'AdZone.description_it'
        db.delete_column(u'advertising_adzone', 'description_it')

        # Deleting field 'AdZone.description_it_markup_type'
        db.delete_column(u'advertising_adzone', 'description_it_markup_type')

        # Deleting field 'AdZone.title_fr'
        db.delete_column(u'advertising_adzone', 'title_fr')

        # Deleting field 'AdZone.title_pl'
        db.delete_column(u'advertising_adzone', 'title_pl')

        # Deleting field 'AdZone.title_tr'
        db.delete_column(u'advertising_adzone', 'title_tr')

        # Deleting field 'AdZone.title_es'
        db.delete_column(u'advertising_adzone', 'title_es')

        # Deleting field 'AdZone.title_it'
        db.delete_column(u'advertising_adzone', 'title_it')


        # Changing field 'AdZone.description_en'
        db.alter_column(u'advertising_adzone', 'description_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Beschreibung', rel=None, unique_for_year=None, unique_for_date=None, unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, db_tablespace=''))

        # Changing field 'AdZone.description_de'
        db.alter_column(u'advertising_adzone', 'description_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Beschreibung', rel=None, unique_for_year=None, unique_for_date=None, unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, db_tablespace=''))
        # Adding field 'AdCategory.description_markup_type'
        db.add_column(u'advertising_adcategory', 'description_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Deleting field 'AdCategory.description_fr'
        db.delete_column(u'advertising_adcategory', 'description_fr')

        # Deleting field 'AdCategory.description_fr_markup_type'
        db.delete_column(u'advertising_adcategory', 'description_fr_markup_type')

        # Deleting field 'AdCategory.description_pl'
        db.delete_column(u'advertising_adcategory', 'description_pl')

        # Deleting field 'AdCategory.description_pl_markup_type'
        db.delete_column(u'advertising_adcategory', 'description_pl_markup_type')

        # Deleting field 'AdCategory.description_tr'
        db.delete_column(u'advertising_adcategory', 'description_tr')

        # Deleting field 'AdCategory.description_tr_markup_type'
        db.delete_column(u'advertising_adcategory', 'description_tr_markup_type')

        # Deleting field 'AdCategory.description_es'
        db.delete_column(u'advertising_adcategory', 'description_es')

        # Deleting field 'AdCategory.description_es_markup_type'
        db.delete_column(u'advertising_adcategory', 'description_es_markup_type')

        # Deleting field 'AdCategory.description_it'
        db.delete_column(u'advertising_adcategory', 'description_it')

        # Deleting field 'AdCategory.description_it_markup_type'
        db.delete_column(u'advertising_adcategory', 'description_it_markup_type')

        # Deleting field 'AdCategory.title_fr'
        db.delete_column(u'advertising_adcategory', 'title_fr')

        # Deleting field 'AdCategory.title_pl'
        db.delete_column(u'advertising_adcategory', 'title_pl')

        # Deleting field 'AdCategory.title_tr'
        db.delete_column(u'advertising_adcategory', 'title_tr')

        # Deleting field 'AdCategory.title_es'
        db.delete_column(u'advertising_adcategory', 'title_es')

        # Deleting field 'AdCategory.title_it'
        db.delete_column(u'advertising_adcategory', 'title_it')


        # Changing field 'AdCategory.description_en'
        db.alter_column(u'advertising_adcategory', 'description_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Beschreibung', rel=None, unique_for_year=None, unique_for_date=None, unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, db_tablespace=''))

        # Changing field 'AdCategory.description_de'
        db.alter_column(u'advertising_adcategory', 'description_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Beschreibung', rel=None, unique_for_year=None, unique_for_date=None, unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, db_tablespace=''))
    
    
    models = {
        u'advertising.adbase': {
            'Meta': {'object_name': 'AdBase'},
            'advertiser': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['advertising.Advertiser']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['advertising.AdCategory']", 'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'adbase_creator'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'adbase_modifier'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'start_showing': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'stop_showing': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(9999, 12, 29, 0, 0)'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['advertising.AdZone']"})
        },
        u'advertising.adcategory': {
            'Meta': {'ordering': "('title',)", 'object_name': 'AdCategory'},
            'description': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'description_de': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_es': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_es_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_fr': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_fr_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_it': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_it_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_pl': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_pl_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_tr': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_tr_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sysname': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_es': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_fr': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_it': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_pl': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_tr': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        u'advertising.adclick': {
            'Meta': {'object_name': 'AdClick'},
            'ad': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['advertising.AdBase']"}),
            'click_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'})
        },
        u'advertising.adimpression': {
            'Meta': {'object_name': 'AdImpression'},
            'ad': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['advertising.AdBase']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impression_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'source_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'})
        },
        u'advertising.advertiser': {
            'Meta': {'ordering': "('company_name',)", 'object_name': 'Advertiser'},
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'advertising.adzone': {
            'Meta': {'ordering': "('title',)", 'object_name': 'AdZone'},
            'description': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'description_de': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_es': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_es_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_fr': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_fr_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_it': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_it_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_pl': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_pl_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_tr': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_tr_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sysname': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_es': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_fr': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_it': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_pl': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_tr': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        u'advertising.bannerad': {
            'Meta': {'object_name': 'BannerAd', '_ormbases': [u'advertising.AdBase']},
            u'adbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['advertising.AdBase']", 'unique': 'True', 'primary_key': 'True'}),
            'content': ('filebrowser.fields.FileBrowseField', [], {'directory': "'advertising/'", 'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png']"})
        },
        u'advertising.textad': {
            'Meta': {'object_name': 'TextAd', '_ormbases': [u'advertising.AdBase']},
            u'adbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['advertising.AdBase']", 'unique': 'True', 'primary_key': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'ordering': "('username',)", 'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('app_label', 'name')", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'permissions.rowlevelpermission': {
            'Meta': {'object_name': 'RowLevelPermission', 'db_table': "'auth_rowlevelpermission'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'negative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'owner_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owner'", 'to': u"orm['contenttypes.ContentType']"}),
            'owner_object_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Permission']"})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['advertising']
