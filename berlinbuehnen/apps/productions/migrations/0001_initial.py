# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'LanguageAndSubtitles'
        db.create_table(u'productions_languageandsubtitles', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=200, null=True)),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('title_de', self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=200, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('title_en', self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=200, db_tablespace='', blank=True, unique=False, db_index=False)),
        )))
        db.send_create_signal(u'productions', ['LanguageAndSubtitles'])

        # Adding model 'ProductionCategory'
        db.create_table(u'productions_productioncategory', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(to=orm['productions.ProductionCategory'], null=True, blank=True)),
            ('title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=200, null=True)),
            ('title_de', self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=200, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('title_en', self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=200, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        )))
        db.send_create_signal(u'productions', ['ProductionCategory'])

        # Adding model 'ProductionCharacteristics'
        db.create_table(u'productions_productioncharacteristics', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=200, null=True)),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('title_de', self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=200, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('title_en', self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=200, db_tablespace='', blank=True, unique=False, db_index=False)),
        )))
        db.send_create_signal(u'productions', ['ProductionCharacteristics'])

        # Adding model 'Production'
        db.create_table(u'productions_production', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='production_creator', null=True, to=orm['auth.User'])),
            ('modifier', self.gf('django.db.models.fields.related.ForeignKey')(related_name='production_modifier', null=True, to=orm['auth.User'])),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('prefix', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True)),
            ('title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True)),
            ('subtitle', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True, blank=True)),
            ('original', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True)),
            ('website', self.gf('base_libs.models.fields.URLField')(max_length=200, blank=True)),
            ('location_title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('street_address', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('street_address2', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(default='Berlin', max_length=255, blank=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('description', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True)),
            ('teaser', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True)),
            ('work_info', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True)),
            ('contents', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True)),
            ('press_text', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True)),
            ('credits', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True)),
            ('language_and_subtitles', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['productions.LanguageAndSubtitles'], null=True, blank=True)),
            ('free_entrance', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('price_from', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('price_till', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('tickets_website', self.gf('base_libs.models.fields.URLField')(max_length=200, blank=True)),
            ('price_information', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True)),
            ('age_from', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('age_till', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('edu_offer_website', self.gf('base_libs.models.fields.URLField')(max_length=200, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='draft', max_length=20, blank=True)),
            ('subtitle_de', self.gf('django.db.models.fields.CharField')(u'Subtitle', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('subtitle_en', self.gf('django.db.models.fields.CharField')(u'Subtitle', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('prefix_de', self.gf('django.db.models.fields.CharField')(u'Title prefix', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('prefix_en', self.gf('django.db.models.fields.CharField')(u'Title prefix', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('contents_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Contents', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('contents_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('contents_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Contents', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('contents_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('title_de', self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('title_en', self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('press_text_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Press text', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('press_text_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('press_text_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Press text', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('press_text_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('description_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('description_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('description_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('description_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('credits_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Credits', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('credits_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('credits_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Credits', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('credits_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('teaser_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Teaser', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('teaser_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('teaser_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Teaser', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('teaser_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('work_info_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Work info', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('work_info_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('work_info_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Work info', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('work_info_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('price_information_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Additional price information', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('price_information_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('price_information_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Additional price information', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('price_information_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('original_de', self.gf('django.db.models.fields.CharField')(u'Original title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('original_en', self.gf('django.db.models.fields.CharField')(u'Original title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
        )))
        db.send_create_signal(u'productions', ['Production'])
        # Adding M2M table for field in_program_of on 'Production'
        m2m_table_name = db.shorten_name(u'productions_production_in_program_of')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('production', models.ForeignKey(orm[u'productions.production'], null=False)),
            ('location', models.ForeignKey(orm[u'locations.location'], null=False))
        ))
        db.create_unique(m2m_table_name, ['production_id', 'location_id'])

        # Adding M2M table for field ensembles on 'Production'
        m2m_table_name = db.shorten_name(u'productions_production_ensembles')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('production', models.ForeignKey(orm[u'productions.production'], null=False)),
            ('location', models.ForeignKey(orm[u'locations.location'], null=False))
        ))
        db.create_unique(m2m_table_name, ['production_id', 'location_id'])

        # Adding M2M table for field play_locations on 'Production'
        m2m_table_name = db.shorten_name(u'productions_production_play_locations')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('production', models.ForeignKey(orm[u'productions.production'], null=False)),
            ('location', models.ForeignKey(orm[u'locations.location'], null=False))
        ))
        db.create_unique(m2m_table_name, ['production_id', 'location_id'])

        # Adding M2M table for field play_stages on 'Production'
        m2m_table_name = db.shorten_name(u'productions_production_play_stages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('production', models.ForeignKey(orm[u'productions.production'], null=False)),
            ('stage', models.ForeignKey(orm[u'locations.stage'], null=False))
        ))
        db.create_unique(m2m_table_name, ['production_id', 'stage_id'])

        # Adding M2M table for field organizers on 'Production'
        m2m_table_name = db.shorten_name(u'productions_production_organizers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('production', models.ForeignKey(orm[u'productions.production'], null=False)),
            ('location', models.ForeignKey(orm[u'locations.location'], null=False))
        ))
        db.create_unique(m2m_table_name, ['production_id', 'location_id'])

        # Adding M2M table for field in_cooperation_with on 'Production'
        m2m_table_name = db.shorten_name(u'productions_production_in_cooperation_with')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('production', models.ForeignKey(orm[u'productions.production'], null=False)),
            ('location', models.ForeignKey(orm[u'locations.location'], null=False))
        ))
        db.create_unique(m2m_table_name, ['production_id', 'location_id'])

        # Adding M2M table for field categories on 'Production'
        m2m_table_name = db.shorten_name(u'productions_production_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('production', models.ForeignKey(orm[u'productions.production'], null=False)),
            ('productioncategory', models.ForeignKey(orm[u'productions.productioncategory'], null=False))
        ))
        db.create_unique(m2m_table_name, ['production_id', 'productioncategory_id'])

        # Adding M2M table for field festivals on 'Production'
        m2m_table_name = db.shorten_name(u'productions_production_festivals')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('production', models.ForeignKey(orm[u'productions.production'], null=False)),
            ('festival', models.ForeignKey(orm[u'festivals.festival'], null=False))
        ))
        db.create_unique(m2m_table_name, ['production_id', 'festival_id'])

        # Adding M2M table for field related_productions on 'Production'
        m2m_table_name = db.shorten_name(u'productions_production_related_productions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_production', models.ForeignKey(orm[u'productions.production'], null=False)),
            ('to_production', models.ForeignKey(orm[u'productions.production'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_production_id', 'to_production_id'])

        # Adding M2M table for field characteristics on 'Production'
        m2m_table_name = db.shorten_name(u'productions_production_characteristics')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('production', models.ForeignKey(orm[u'productions.production'], null=False)),
            ('productioncharacteristics', models.ForeignKey(orm[u'productions.productioncharacteristics'], null=False))
        ))
        db.create_unique(m2m_table_name, ['production_id', 'productioncharacteristics_id'])

        # Adding M2M table for field sponsors on 'Production'
        m2m_table_name = db.shorten_name(u'productions_production_sponsors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('production', models.ForeignKey(orm[u'productions.production'], null=False)),
            ('sponsor', models.ForeignKey(orm[u'sponsors.sponsor'], null=False))
        ))
        db.create_unique(m2m_table_name, ['production_id', 'sponsor_id'])


        # Adding model 'ProductionVideo'
        db.create_table(u'productions_productionvideo', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('production', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['productions.Production'])),
            ('link_or_embed', self.gf('django.db.models.fields.TextField')()),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(default=None)),
        )))
        db.send_create_signal(u'productions', ['ProductionVideo'])

        # Adding model 'ProductionImage'
        db.create_table(u'productions_productionimage', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('production', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['productions.Production'])),
            ('path', self.gf('filebrowser.fields.FileBrowseField')(directory='productions/', max_length=255, extensions=['.jpg', '.jpeg', '.gif', '.png'])),
            ('copyright_restrictions', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(default=None)),
        )))
        db.send_create_signal(u'productions', ['ProductionImage'])

        # Adding model 'ProductionPDF'
        db.create_table(u'productions_productionpdf', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('production', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['productions.Production'])),
            ('path', self.gf('filebrowser.fields.FileBrowseField')(directory='productions/', max_length=255, extensions=['.pdf'])),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(default=None)),
        )))
        db.send_create_signal(u'productions', ['ProductionPDF'])

        # Adding model 'ProductionLeadership'
        db.create_table(u'productions_productionleadership', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('production', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['productions.Production'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Person'])),
            ('function', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True, blank=True)),
            ('function_de', self.gf('django.db.models.fields.CharField')(u'Function', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('function_en', self.gf('django.db.models.fields.CharField')(u'Function', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
        )))
        db.send_create_signal(u'productions', ['ProductionLeadership'])

        # Adding model 'ProductionAuthorship'
        db.create_table(u'productions_productionauthorship', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('production', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['productions.Production'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Person'])),
            ('authorship_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.AuthorshipType'])),
        )))
        db.send_create_signal(u'productions', ['ProductionAuthorship'])

        # Adding model 'ProductionInvolvement'
        db.create_table(u'productions_productioninvolvement', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('production', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['productions.Production'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Person'])),
            ('involvement_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.InvolvementType'])),
            ('involvement_role', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True, blank=True)),
            ('involvement_instrument', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True, blank=True)),
            ('involvement_role_de', self.gf('django.db.models.fields.CharField')(u'Role', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('involvement_role_en', self.gf('django.db.models.fields.CharField')(u'Role', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('involvement_instrument_de', self.gf('django.db.models.fields.CharField')(u'Instrument', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('involvement_instrument_en', self.gf('django.db.models.fields.CharField')(u'Instrument', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
        )))
        db.send_create_signal(u'productions', ['ProductionInvolvement'])

        # Adding model 'EventCharacteristics'
        db.create_table(u'productions_eventcharacteristics', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=200, null=True)),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('title_de', self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=200, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('title_en', self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=200, db_tablespace='', blank=True, unique=False, db_index=False)),
        )))
        db.send_create_signal(u'productions', ['EventCharacteristics'])

        # Adding model 'Event'
        db.create_table(u'productions_event', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='event_creator', null=True, to=orm['auth.User'])),
            ('modifier', self.gf('django.db.models.fields.related.ForeignKey')(related_name='event_modifier', null=True, to=orm['auth.User'])),
            ('production', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['productions.Production'])),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('start_time', self.gf('django.db.models.fields.TimeField')()),
            ('end_time', self.gf('django.db.models.fields.TimeField')()),
            ('duration', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pauses', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('location_title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('street_address', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('street_address2', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(default='Berlin', max_length=255, blank=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('description', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True)),
            ('teaser', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True)),
            ('work_info', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True)),
            ('contents', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True)),
            ('press_text', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True)),
            ('credits', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True)),
            ('event_status', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('ticket_status', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('other_characteristics', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True)),
            ('contents_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Contents', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('contents_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('contents_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Contents', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('contents_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('press_text_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Press text', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('press_text_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('press_text_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Press text', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('press_text_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('description_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('description_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('description_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('description_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('credits_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Credits', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('credits_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('credits_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Credits', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('credits_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('teaser_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Teaser', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('teaser_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('teaser_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Teaser', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('teaser_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('work_info_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Work info', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('work_info_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('work_info_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Work info', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('work_info_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('other_characteristics_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Other characteristics', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('other_characteristics_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('other_characteristics_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Other characteristics', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('other_characteristics_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
        )))
        db.send_create_signal(u'productions', ['Event'])
        # Adding M2M table for field play_locations on 'Event'
        m2m_table_name = db.shorten_name(u'productions_event_play_locations')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'productions.event'], null=False)),
            ('location', models.ForeignKey(orm[u'locations.location'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'location_id'])

        # Adding M2M table for field play_stages on 'Event'
        m2m_table_name = db.shorten_name(u'productions_event_play_stages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'productions.event'], null=False)),
            ('stage', models.ForeignKey(orm[u'locations.stage'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'stage_id'])

        # Adding M2M table for field characteristics on 'Event'
        m2m_table_name = db.shorten_name(u'productions_event_characteristics')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'productions.event'], null=False)),
            ('eventcharacteristics', models.ForeignKey(orm[u'productions.eventcharacteristics'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'eventcharacteristics_id'])


        # Adding model 'EventVideo'
        db.create_table(u'productions_eventvideo', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['productions.Event'])),
            ('link_or_embed', self.gf('django.db.models.fields.TextField')()),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(default=None)),
        )))
        db.send_create_signal(u'productions', ['EventVideo'])

        # Adding model 'EventImage'
        db.create_table(u'productions_eventimage', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['productions.Event'])),
            ('path', self.gf('filebrowser.fields.FileBrowseField')(directory='events/', max_length=255, extensions=['.jpg', '.jpeg', '.gif', '.png'])),
            ('copyright_restrictions', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(default=None)),
        )))
        db.send_create_signal(u'productions', ['EventImage'])

        # Adding model 'EventPDF'
        db.create_table(u'productions_eventpdf', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['productions.Event'])),
            ('path', self.gf('filebrowser.fields.FileBrowseField')(directory='events/', max_length=255, extensions=['.pdf'])),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(default=None)),
        )))
        db.send_create_signal(u'productions', ['EventPDF'])

        # Adding model 'EventLeadership'
        db.create_table(u'productions_eventleadership', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['productions.Event'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Person'])),
            ('function', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True, blank=True)),
            ('function_de', self.gf('django.db.models.fields.CharField')(u'Function', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('function_en', self.gf('django.db.models.fields.CharField')(u'Function', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
        )))
        db.send_create_signal(u'productions', ['EventLeadership'])

        # Adding model 'EventAuthorship'
        db.create_table(u'productions_eventauthorship', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['productions.Event'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Person'])),
            ('authorship_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.AuthorshipType'])),
        )))
        db.send_create_signal(u'productions', ['EventAuthorship'])

        # Adding model 'EventInvolvement'
        db.create_table(u'productions_eventinvolvement', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['productions.Event'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Person'])),
            ('involvement_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.InvolvementType'])),
            ('involvement_role', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True, blank=True)),
            ('involvement_instrument', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True, blank=True)),
            ('involvement_role_de', self.gf('django.db.models.fields.CharField')(u'Role', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('involvement_role_en', self.gf('django.db.models.fields.CharField')(u'Role', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('involvement_instrument_de', self.gf('django.db.models.fields.CharField')(u'Instrument', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('involvement_instrument_en', self.gf('django.db.models.fields.CharField')(u'Instrument', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
        )))
        db.send_create_signal(u'productions', ['EventInvolvement'])
    
    
    def backwards(self, orm):
                # Deleting model 'LanguageAndSubtitles'
        db.delete_table(u'productions_languageandsubtitles')

        # Deleting model 'ProductionCategory'
        db.delete_table(u'productions_productioncategory')

        # Deleting model 'ProductionCharacteristics'
        db.delete_table(u'productions_productioncharacteristics')

        # Deleting model 'Production'
        db.delete_table(u'productions_production')

        # Removing M2M table for field in_program_of on 'Production'
        db.delete_table(db.shorten_name(u'productions_production_in_program_of'))

        # Removing M2M table for field ensembles on 'Production'
        db.delete_table(db.shorten_name(u'productions_production_ensembles'))

        # Removing M2M table for field play_locations on 'Production'
        db.delete_table(db.shorten_name(u'productions_production_play_locations'))

        # Removing M2M table for field play_stages on 'Production'
        db.delete_table(db.shorten_name(u'productions_production_play_stages'))

        # Removing M2M table for field organizers on 'Production'
        db.delete_table(db.shorten_name(u'productions_production_organizers'))

        # Removing M2M table for field in_cooperation_with on 'Production'
        db.delete_table(db.shorten_name(u'productions_production_in_cooperation_with'))

        # Removing M2M table for field categories on 'Production'
        db.delete_table(db.shorten_name(u'productions_production_categories'))

        # Removing M2M table for field festivals on 'Production'
        db.delete_table(db.shorten_name(u'productions_production_festivals'))

        # Removing M2M table for field related_productions on 'Production'
        db.delete_table(db.shorten_name(u'productions_production_related_productions'))

        # Removing M2M table for field characteristics on 'Production'
        db.delete_table(db.shorten_name(u'productions_production_characteristics'))

        # Removing M2M table for field sponsors on 'Production'
        db.delete_table(db.shorten_name(u'productions_production_sponsors'))

        # Deleting model 'ProductionVideo'
        db.delete_table(u'productions_productionvideo')

        # Deleting model 'ProductionImage'
        db.delete_table(u'productions_productionimage')

        # Deleting model 'ProductionPDF'
        db.delete_table(u'productions_productionpdf')

        # Deleting model 'ProductionLeadership'
        db.delete_table(u'productions_productionleadership')

        # Deleting model 'ProductionAuthorship'
        db.delete_table(u'productions_productionauthorship')

        # Deleting model 'ProductionInvolvement'
        db.delete_table(u'productions_productioninvolvement')

        # Deleting model 'EventCharacteristics'
        db.delete_table(u'productions_eventcharacteristics')

        # Deleting model 'Event'
        db.delete_table(u'productions_event')

        # Removing M2M table for field play_locations on 'Event'
        db.delete_table(db.shorten_name(u'productions_event_play_locations'))

        # Removing M2M table for field play_stages on 'Event'
        db.delete_table(db.shorten_name(u'productions_event_play_stages'))

        # Removing M2M table for field characteristics on 'Event'
        db.delete_table(db.shorten_name(u'productions_event_characteristics'))

        # Deleting model 'EventVideo'
        db.delete_table(u'productions_eventvideo')

        # Deleting model 'EventImage'
        db.delete_table(u'productions_eventimage')

        # Deleting model 'EventPDF'
        db.delete_table(u'productions_eventpdf')

        # Deleting model 'EventLeadership'
        db.delete_table(u'productions_eventleadership')

        # Deleting model 'EventAuthorship'
        db.delete_table(u'productions_eventauthorship')

        # Deleting model 'EventInvolvement'
        db.delete_table(u'productions_eventinvolvement')

    
    
    models = {
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
        u'festivals.festival': {
            'Meta': {'ordering': "['title']", 'object_name': 'Festival'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'festival_creator'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'description': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'description_de': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'end': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'festival_modifier'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'start': ('django.db.models.fields.DateField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'draft'", 'max_length': '20', 'blank': 'True'}),
            'subtitle': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subtitle_de': ('django.db.models.fields.CharField', ["u'Subtitle'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'subtitle_en': ('django.db.models.fields.CharField', ["u'Subtitle'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'website': ('base_libs.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'locations.accessibilityoption': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'AccessibilityOption'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'directory': "'accessibility/'", 'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png']", 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '200', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        u'locations.location': {
            'Meta': {'ordering': "['title']", 'object_name': 'Location'},
            'accessibility_options': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['locations.AccessibilityOption']", 'symmetrical': 'False', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "'Berlin'", 'max_length': '255'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'location_creator'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'description': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'description_de': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'blank': 'True'}),
            'fax_area': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'fax_country': ('django.db.models.fields.CharField', [], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'fax_number': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'location_modifier'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'phone_area': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'phone_country': ('django.db.models.fields.CharField', [], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['locations.Service']", 'symmetrical': 'False', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'draft'", 'max_length': '20', 'blank': 'True'}),
            'street_address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'street_address2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'subtitle': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subtitle_de': ('django.db.models.fields.CharField', ["u'Subtitle'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'subtitle_en': ('django.db.models.fields.CharField', ["u'Subtitle'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'tickets_city': ('django.db.models.fields.CharField', [], {'default': "'Berlin'", 'max_length': '255', 'blank': 'True'}),
            'tickets_email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'blank': 'True'}),
            'tickets_postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'tickets_street_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'tickets_street_address2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'tickets_website': ('base_libs.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'website': ('base_libs.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'locations.service': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'Service'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'directory': "'services/'", 'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png']", 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '200', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        u'locations.stage': {
            'Meta': {'ordering': "['title']", 'object_name': 'Stage'},
            'city': ('django.db.models.fields.CharField', [], {'default': "'Berlin'", 'max_length': '255', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stage_creator'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'description': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'description_de': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['locations.Location']"}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stage_modifier'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'street_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'street_address2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        u'people.authorshiptype': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'AuthorshipType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        u'people.involvementtype': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'InvolvementType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        u'people.person': {
            'Meta': {'ordering': "['last_name', 'first_name']", 'object_name': 'Person'},
            'authorship_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.AuthorshipType']", 'max_length': '255', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'person_creator'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'involvement_instrument': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'involvement_instrument_de': ('django.db.models.fields.CharField', ["u'Default involvement instrument'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'involvement_instrument_en': ('django.db.models.fields.CharField', ["u'Default involvement instrument'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'involvement_role': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'involvement_role_de': ('django.db.models.fields.CharField', ["u'Default involvement role'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'involvement_role_en': ('django.db.models.fields.CharField', ["u'Default involvement role'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'involvement_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.InvolvementType']", 'max_length': '255', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'leadership_function': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'leadership_function_de': ('django.db.models.fields.CharField', ["u'Default leadership function'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'leadership_function_en': ('django.db.models.fields.CharField', ["u'Default leadership function'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'person_modifier'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'prefix': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.Prefix']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'draft'", 'max_length': '20', 'blank': 'True'})
        },
        u'people.prefix': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'Prefix'},
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
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
        },
        u'productions.event': {
            'Meta': {'ordering': "['start_date', 'start_time']", 'object_name': 'Event'},
            'characteristics': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['productions.EventCharacteristics']", 'symmetrical': 'False', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "'Berlin'", 'max_length': '255', 'blank': 'True'}),
            'contents': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'contents_de': ('base_libs.models.fields.ExtendedTextField', ["u'Contents'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'contents_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'contents_en': ('base_libs.models.fields.ExtendedTextField', ["u'Contents'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'contents_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'event_creator'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'credits': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'credits_de': ('base_libs.models.fields.ExtendedTextField', ["u'Credits'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'credits_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'credits_en': ('base_libs.models.fields.ExtendedTextField', ["u'Credits'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'credits_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'description_de': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'duration': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            'event_status': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'location_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'event_modifier'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'other_characteristics': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'other_characteristics_de': ('base_libs.models.fields.ExtendedTextField', ["u'Other characteristics'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'other_characteristics_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'other_characteristics_en': ('base_libs.models.fields.ExtendedTextField', ["u'Other characteristics'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'other_characteristics_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'pauses': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'play_locations': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['locations.Location']", 'symmetrical': 'False', 'blank': 'True'}),
            'play_stages': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['locations.Stage']", 'symmetrical': 'False', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'press_text': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'press_text_de': ('base_libs.models.fields.ExtendedTextField', ["u'Press text'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'press_text_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'press_text_en': ('base_libs.models.fields.ExtendedTextField', ["u'Press text'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'press_text_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['productions.Production']"}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'start_time': ('django.db.models.fields.TimeField', [], {}),
            'street_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'street_address2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'teaser': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'teaser_de': ('base_libs.models.fields.ExtendedTextField', ["u'Teaser'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'teaser_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'teaser_en': ('base_libs.models.fields.ExtendedTextField', ["u'Teaser'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'teaser_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'ticket_status': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'work_info': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'work_info_de': ('base_libs.models.fields.ExtendedTextField', ["u'Work info'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'work_info_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'work_info_en': ('base_libs.models.fields.ExtendedTextField', ["u'Work info'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'work_info_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'})
        },
        u'productions.eventauthorship': {
            'Meta': {'ordering': "['person__last_name', 'person__first_name']", 'object_name': 'EventAuthorship'},
            'authorship_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.AuthorshipType']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['productions.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.Person']"})
        },
        u'productions.eventcharacteristics': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'EventCharacteristics'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '200', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        u'productions.eventimage': {
            'Meta': {'ordering': "['sort_order', 'creation_date']", 'object_name': 'EventImage'},
            'copyright_restrictions': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['productions.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'path': ('filebrowser.fields.FileBrowseField', [], {'directory': "'events/'", 'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png']"}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': 'None'})
        },
        u'productions.eventinvolvement': {
            'Meta': {'ordering': "['person__last_name', 'person__first_name']", 'object_name': 'EventInvolvement'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['productions.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'involvement_instrument': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'involvement_instrument_de': ('django.db.models.fields.CharField', ["u'Instrument'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'involvement_instrument_en': ('django.db.models.fields.CharField', ["u'Instrument'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'involvement_role': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'involvement_role_de': ('django.db.models.fields.CharField', ["u'Role'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'involvement_role_en': ('django.db.models.fields.CharField', ["u'Role'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'involvement_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.InvolvementType']"}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.Person']"})
        },
        u'productions.eventleadership': {
            'Meta': {'ordering': "['person__last_name', 'person__first_name']", 'object_name': 'EventLeadership'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['productions.Event']"}),
            'function': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'function_de': ('django.db.models.fields.CharField', ["u'Function'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'function_en': ('django.db.models.fields.CharField', ["u'Function'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.Person']"})
        },
        u'productions.eventpdf': {
            'Meta': {'ordering': "['sort_order', 'creation_date']", 'object_name': 'EventPDF'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['productions.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'path': ('filebrowser.fields.FileBrowseField', [], {'directory': "'events/'", 'max_length': '255', 'extensions': "['.pdf']"}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': 'None'})
        },
        u'productions.eventvideo': {
            'Meta': {'ordering': "['sort_order', 'creation_date']", 'object_name': 'EventVideo'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['productions.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_or_embed': ('django.db.models.fields.TextField', [], {}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': 'None'})
        },
        u'productions.languageandsubtitles': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'LanguageAndSubtitles'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '200', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        u'productions.production': {
            'Meta': {'ordering': "['title']", 'object_name': 'Production'},
            'age_from': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'age_till': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'categories': ('mptt.fields.TreeManyToManyField', [], {'to': u"orm['productions.ProductionCategory']", 'symmetrical': 'False', 'blank': 'True'}),
            'characteristics': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['productions.ProductionCharacteristics']", 'symmetrical': 'False', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "'Berlin'", 'max_length': '255', 'blank': 'True'}),
            'contents': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'contents_de': ('base_libs.models.fields.ExtendedTextField', ["u'Contents'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'contents_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'contents_en': ('base_libs.models.fields.ExtendedTextField', ["u'Contents'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'contents_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'production_creator'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'credits': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'credits_de': ('base_libs.models.fields.ExtendedTextField', ["u'Credits'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'credits_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'credits_en': ('base_libs.models.fields.ExtendedTextField', ["u'Credits'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'credits_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'description_de': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'edu_offer_website': ('base_libs.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'ensembles': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'ensembled_productions'", 'blank': 'True', 'to': u"orm['locations.Location']"}),
            'festivals': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['festivals.Festival']", 'symmetrical': 'False', 'blank': 'True'}),
            'free_entrance': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_cooperation_with': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'cooperated_productions'", 'blank': 'True', 'to': u"orm['locations.Location']"}),
            'in_program_of': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'program_productions'", 'blank': 'True', 'to': u"orm['locations.Location']"}),
            'language_and_subtitles': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['productions.LanguageAndSubtitles']", 'null': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'location_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'production_modifier'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'organizers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'organized_productions'", 'blank': 'True', 'to': u"orm['locations.Location']"}),
            'original': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'original_de': ('django.db.models.fields.CharField', ["u'Original title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'original_en': ('django.db.models.fields.CharField', ["u'Original title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'play_locations': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'located_productions'", 'blank': 'True', 'to': u"orm['locations.Location']"}),
            'play_stages': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['locations.Stage']", 'symmetrical': 'False', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'prefix': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'prefix_de': ('django.db.models.fields.CharField', ["u'Title prefix'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'prefix_en': ('django.db.models.fields.CharField', ["u'Title prefix'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'press_text': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'press_text_de': ('base_libs.models.fields.ExtendedTextField', ["u'Press text'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'press_text_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'press_text_en': ('base_libs.models.fields.ExtendedTextField', ["u'Press text'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'press_text_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'price_from': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'price_information': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'price_information_de': ('base_libs.models.fields.ExtendedTextField', ["u'Additional price information'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'price_information_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'price_information_en': ('base_libs.models.fields.ExtendedTextField', ["u'Additional price information'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'price_information_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'price_till': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'related_productions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_productions_rel_+'", 'to': u"orm['productions.Production']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sponsors': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sponsors.Sponsor']", 'symmetrical': 'False', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'draft'", 'max_length': '20', 'blank': 'True'}),
            'street_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'street_address2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'subtitle': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subtitle_de': ('django.db.models.fields.CharField', ["u'Subtitle'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'subtitle_en': ('django.db.models.fields.CharField', ["u'Subtitle'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'teaser': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'teaser_de': ('base_libs.models.fields.ExtendedTextField', ["u'Teaser'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'teaser_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'teaser_en': ('base_libs.models.fields.ExtendedTextField', ["u'Teaser'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'teaser_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'tickets_website': ('base_libs.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'website': ('base_libs.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'work_info': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'work_info_de': ('base_libs.models.fields.ExtendedTextField', ["u'Work info'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'work_info_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'work_info_en': ('base_libs.models.fields.ExtendedTextField', ["u'Work info'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'work_info_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'})
        },
        u'productions.productionauthorship': {
            'Meta': {'ordering': "['person__last_name', 'person__first_name']", 'object_name': 'ProductionAuthorship'},
            'authorship_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.AuthorshipType']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.Person']"}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['productions.Production']"})
        },
        u'productions.productioncategory': {
            'Meta': {'ordering': "['tree_id', 'lft']", 'object_name': 'ProductionCategory'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'to': u"orm['productions.ProductionCategory']", 'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '200', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'productions.productioncharacteristics': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'ProductionCharacteristics'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '200', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        u'productions.productionimage': {
            'Meta': {'ordering': "['sort_order', 'creation_date']", 'object_name': 'ProductionImage'},
            'copyright_restrictions': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'path': ('filebrowser.fields.FileBrowseField', [], {'directory': "'productions/'", 'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png']"}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['productions.Production']"}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': 'None'})
        },
        u'productions.productioninvolvement': {
            'Meta': {'ordering': "['person__last_name', 'person__first_name']", 'object_name': 'ProductionInvolvement'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'involvement_instrument': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'involvement_instrument_de': ('django.db.models.fields.CharField', ["u'Instrument'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'involvement_instrument_en': ('django.db.models.fields.CharField', ["u'Instrument'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'involvement_role': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'involvement_role_de': ('django.db.models.fields.CharField', ["u'Role'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'involvement_role_en': ('django.db.models.fields.CharField', ["u'Role'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'involvement_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.InvolvementType']"}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.Person']"}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['productions.Production']"})
        },
        u'productions.productionleadership': {
            'Meta': {'ordering': "['person__last_name', 'person__first_name']", 'object_name': 'ProductionLeadership'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'function': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'function_de': ('django.db.models.fields.CharField', ["u'Function'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'function_en': ('django.db.models.fields.CharField', ["u'Function'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.Person']"}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['productions.Production']"})
        },
        u'productions.productionpdf': {
            'Meta': {'ordering': "['sort_order', 'creation_date']", 'object_name': 'ProductionPDF'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'path': ('filebrowser.fields.FileBrowseField', [], {'directory': "'productions/'", 'max_length': '255', 'extensions': "['.pdf']"}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['productions.Production']"}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': 'None'})
        },
        u'productions.productionvideo': {
            'Meta': {'ordering': "['sort_order', 'creation_date']", 'object_name': 'ProductionVideo'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_or_embed': ('django.db.models.fields.TextField', [], {}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['productions.Production']"}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': 'None'})
        },
        u'sponsors.sponsor': {
            'Meta': {'ordering': "['title']", 'object_name': 'Sponsor'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'directory': "'sponsors/'", 'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png']"}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'draft'", 'max_length': '20', 'blank': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'website': ('base_libs.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['productions']
