# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('museums', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='museum',
            name='accessibility_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Barrierefreiheit', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='accessibility_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Barrierefreiheit', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='accessibility_es',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Barrierefreiheit', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='accessibility_fr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Barrierefreiheit', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='accessibility_it',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Barrierefreiheit', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='accessibility_pl',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Barrierefreiheit', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='accessibility_tr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Barrierefreiheit', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='admission_price_info_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='admission_price_info_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='admission_price_info_es',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='admission_price_info_fr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='admission_price_info_it',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='admission_price_info_pl',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='admission_price_info_tr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='description_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='description_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='description_es',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='description_fr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='description_it',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='description_pl',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='description_tr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='free_entrance',
            field=models.BooleanField(default=False, verbose_name='Free entrance'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='group_ticket_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Gruppenticket', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='group_ticket_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Gruppenticket', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='group_ticket_es',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Gruppenticket', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='group_ticket_fr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Gruppenticket', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='group_ticket_it',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Gruppenticket', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='group_ticket_pl',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Gruppenticket', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='group_ticket_tr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Gruppenticket', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='has_audioguide',
            field=models.BooleanField(default=False, verbose_name='Audioguide'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='has_audioguide_de',
            field=models.BooleanField(default=False, verbose_name='German'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='has_audioguide_en',
            field=models.BooleanField(default=False, verbose_name='English'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='has_audioguide_for_children',
            field=models.BooleanField(default=False, verbose_name='Audioguide for children'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='has_audioguide_for_learning_difficulties',
            field=models.BooleanField(default=False, verbose_name='Audioguide for people with learning difficulties'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='has_audioguide_fr',
            field=models.BooleanField(default=False, verbose_name='French'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='has_audioguide_it',
            field=models.BooleanField(default=False, verbose_name='Italian'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='has_audioguide_pl',
            field=models.BooleanField(default=False, verbose_name='Polish'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='has_audioguide_sp',
            field=models.BooleanField(default=False, verbose_name='Spanish'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='has_audioguide_tr',
            field=models.BooleanField(default=False, verbose_name='Turkish'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='image_caption_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', editable=False, max_length=255, blank=True, null=True, verbose_name='Bildbeschreibung'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='image_caption_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', editable=False, max_length=255, blank=True, null=True, verbose_name='Bildbeschreibung'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='image_caption_es',
            field=base_libs.models.fields.ExtendedTextField(default=b'', editable=False, max_length=255, blank=True, null=True, verbose_name='Bildbeschreibung'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='image_caption_fr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', editable=False, max_length=255, blank=True, null=True, verbose_name='Bildbeschreibung'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='image_caption_it',
            field=base_libs.models.fields.ExtendedTextField(default=b'', editable=False, max_length=255, blank=True, null=True, verbose_name='Bildbeschreibung'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='image_caption_pl',
            field=base_libs.models.fields.ExtendedTextField(default=b'', editable=False, max_length=255, blank=True, null=True, verbose_name='Bildbeschreibung'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='image_caption_tr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', editable=False, max_length=255, blank=True, null=True, verbose_name='Bildbeschreibung'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='is_for_children',
            field=models.BooleanField(default=False, verbose_name='Special for children'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='member_of_museumspass',
            field=models.BooleanField(default=False, verbose_name='Museumspass Berlin'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='open_on_mondays',
            field=models.BooleanField(default=False, verbose_name='Open on Mondays'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='reduced_price_info_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis erm\xe4\xdfigt Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='reduced_price_info_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis erm\xe4\xdfigt Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='reduced_price_info_es',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis erm\xe4\xdfigt Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='reduced_price_info_fr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis erm\xe4\xdfigt Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='reduced_price_info_it',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis erm\xe4\xdfigt Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='reduced_price_info_pl',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis erm\xe4\xdfigt Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='reduced_price_info_tr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis erm\xe4\xdfigt Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='service_archive',
            field=models.BooleanField(default=False, verbose_name='Archive'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='service_cafe',
            field=models.BooleanField(default=False, verbose_name='Cafe'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='service_diaper_changing_table',
            field=models.BooleanField(default=False, verbose_name='Diaper changing table'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='service_library',
            field=models.BooleanField(default=False, verbose_name='Library'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='service_restaurant',
            field=models.BooleanField(default=False, verbose_name='Restaurant'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='service_shop',
            field=models.BooleanField(default=False, verbose_name='Museum Shop'),
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
            model_name='specialopeningtime',
            name='exceptions_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Sonder\xf6ffnungszeiten', blank=True),
        ),
        migrations.AlterField(
            model_name='specialopeningtime',
            name='exceptions_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Sonder\xf6ffnungszeiten', blank=True),
        ),
        migrations.AlterField(
            model_name='specialopeningtime',
            name='exceptions_es',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Sonder\xf6ffnungszeiten', blank=True),
        ),
        migrations.AlterField(
            model_name='specialopeningtime',
            name='exceptions_fr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Sonder\xf6ffnungszeiten', blank=True),
        ),
        migrations.AlterField(
            model_name='specialopeningtime',
            name='exceptions_it',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Sonder\xf6ffnungszeiten', blank=True),
        ),
        migrations.AlterField(
            model_name='specialopeningtime',
            name='exceptions_pl',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Sonder\xf6ffnungszeiten', blank=True),
        ),
        migrations.AlterField(
            model_name='specialopeningtime',
            name='exceptions_tr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Sonder\xf6ffnungszeiten', blank=True),
        ),
        migrations.AlterField(
            model_name='specialopeningtime',
            name='is_closed',
            field=models.BooleanField(default=False, verbose_name='Closed'),
        ),
        migrations.AlterField(
            model_name='specialopeningtime',
            name='is_regular',
            field=models.BooleanField(default=False, verbose_name='Regular Opening hours'),
        ),
    ]
