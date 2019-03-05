# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('exhibitions', '0002_cms_related'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exhibition',
            name='admission_price_info_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='admission_price_info_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='admission_price_info_es',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='admission_price_info_fr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='admission_price_info_it',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='admission_price_info_pl',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='admission_price_info_tr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='catalog_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Katalog', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='catalog_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Katalog', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='catalog_es',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Katalog', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='catalog_fr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Katalog', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='catalog_it',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Katalog', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='catalog_pl',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Katalog', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='catalog_tr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Katalog', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='closing_soon',
            field=models.BooleanField(default=False, verbose_name='Closing soon'),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='description_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='description_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='description_es',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='description_fr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='description_it',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='description_locked',
            field=models.BooleanField(default=False, help_text="When checked, press text won't be copied automatically to description.", verbose_name='Description locked'),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='description_pl',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='description_tr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='exhibition_extended',
            field=models.BooleanField(default=False, verbose_name='Exhibition extended'),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='featured',
            field=models.BooleanField(default=False, verbose_name='Featured in Newsletter'),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='featured_in_magazine',
            field=models.BooleanField(default=False, verbose_name='Featured in Magazine'),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='free_entrance',
            field=models.BooleanField(default=False, verbose_name='Free entrance'),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='image_caption_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', editable=False, max_length=255, blank=True, null=True, verbose_name='Bildbeschreibung'),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='image_caption_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', editable=False, max_length=255, blank=True, null=True, verbose_name='Bildbeschreibung'),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='image_caption_es',
            field=base_libs.models.fields.ExtendedTextField(default=b'', editable=False, max_length=255, blank=True, null=True, verbose_name='Bildbeschreibung'),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='image_caption_fr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', editable=False, max_length=255, blank=True, null=True, verbose_name='Bildbeschreibung'),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='image_caption_it',
            field=base_libs.models.fields.ExtendedTextField(default=b'', editable=False, max_length=255, blank=True, null=True, verbose_name='Bildbeschreibung'),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='image_caption_pl',
            field=base_libs.models.fields.ExtendedTextField(default=b'', editable=False, max_length=255, blank=True, null=True, verbose_name='Bildbeschreibung'),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='image_caption_tr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', editable=False, max_length=255, blank=True, null=True, verbose_name='Bildbeschreibung'),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='is_for_children',
            field=models.BooleanField(default=False, verbose_name='Special for children / families / youth'),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='museum_opening_hours',
            field=models.BooleanField(default=False, verbose_name='See opening hours from museum'),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='museum_prices',
            field=models.BooleanField(default=False, verbose_name='See prices from museum'),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='newly_opened',
            field=models.BooleanField(default=False, verbose_name='Newly opened'),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='other_locations_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Weitere Ausstellungsorte', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='other_locations_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Weitere Ausstellungsorte', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='other_locations_es',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Weitere Ausstellungsorte', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='other_locations_fr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Weitere Ausstellungsorte', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='other_locations_it',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Weitere Ausstellungsorte', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='other_locations_pl',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Weitere Ausstellungsorte', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='other_locations_tr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Weitere Ausstellungsorte', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='permanent',
            field=models.BooleanField(default=False, verbose_name='Permanent exhibition'),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='press_text_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Pressetext', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='press_text_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Pressetext', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='press_text_es',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Pressetext', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='press_text_fr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Pressetext', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='press_text_it',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Pressetext', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='press_text_pl',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Pressetext', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='press_text_tr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Pressetext', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='reduced_price_info_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis erm\xe4\xdfigt Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='reduced_price_info_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis erm\xe4\xdfigt Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='reduced_price_info_es',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis erm\xe4\xdfigt Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='reduced_price_info_fr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis erm\xe4\xdfigt Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='reduced_price_info_it',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis erm\xe4\xdfigt Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='reduced_price_info_pl',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis erm\xe4\xdfigt Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='reduced_price_info_tr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis erm\xe4\xdfigt Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='special',
            field=models.BooleanField(default=False, verbose_name='Special exhibition'),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='suitable_for_disabled',
            field=models.BooleanField(default=False, verbose_name='Exhibition suitable for people with disabilities'),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='suitable_for_disabled_info_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Spezielle Eignung f\xfcr Menschen mit Behinderung', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='suitable_for_disabled_info_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Spezielle Eignung f\xfcr Menschen mit Behinderung', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='suitable_for_disabled_info_es',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Spezielle Eignung f\xfcr Menschen mit Behinderung', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='suitable_for_disabled_info_fr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Spezielle Eignung f\xfcr Menschen mit Behinderung', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='suitable_for_disabled_info_it',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Spezielle Eignung f\xfcr Menschen mit Behinderung', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='suitable_for_disabled_info_pl',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Spezielle Eignung f\xfcr Menschen mit Behinderung', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='suitable_for_disabled_info_tr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Spezielle Eignung f\xfcr Menschen mit Behinderung', blank=True),
        ),
        migrations.AlterField(
            model_name='season',
            name='exceptions_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Sonder\xf6ffnungszeiten', blank=True),
        ),
        migrations.AlterField(
            model_name='season',
            name='exceptions_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Sonder\xf6ffnungszeiten', blank=True),
        ),
        migrations.AlterField(
            model_name='season',
            name='exceptions_es',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Sonder\xf6ffnungszeiten', blank=True),
        ),
        migrations.AlterField(
            model_name='season',
            name='exceptions_fr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Sonder\xf6ffnungszeiten', blank=True),
        ),
        migrations.AlterField(
            model_name='season',
            name='exceptions_it',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Sonder\xf6ffnungszeiten', blank=True),
        ),
        migrations.AlterField(
            model_name='season',
            name='exceptions_pl',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Sonder\xf6ffnungszeiten', blank=True),
        ),
        migrations.AlterField(
            model_name='season',
            name='exceptions_tr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Sonder\xf6ffnungszeiten', blank=True),
        ),
        migrations.AlterField(
            model_name='season',
            name='is_open_24_7',
            field=models.BooleanField(default=False, verbose_name='Open 24/7'),
        ),
    ]
