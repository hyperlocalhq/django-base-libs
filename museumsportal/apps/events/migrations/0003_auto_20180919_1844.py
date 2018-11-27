# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20180829_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='admission_price_info_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='admission_price_info_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='admission_price_info_es',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='admission_price_info_fr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='admission_price_info_it',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='admission_price_info_pl',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='admission_price_info_tr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='booking_info_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Anmeldung/Buchung', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='booking_info_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Anmeldung/Buchung', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='booking_info_es',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Anmeldung/Buchung', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='booking_info_fr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Anmeldung/Buchung', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='booking_info_it',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Anmeldung/Buchung', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='booking_info_pl',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Anmeldung/Buchung', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='booking_info_tr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Anmeldung/Buchung', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='description_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='description_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='description_es',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='description_fr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='description_it',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='description_locked',
            field=models.BooleanField(default=False, help_text="When checked, press text won't be copied automatically to description.", verbose_name='Description locked'),
        ),
        migrations.AlterField(
            model_name='event',
            name='description_pl',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='description_tr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='featured',
            field=models.BooleanField(default=False, verbose_name='Featured in Newsletter'),
        ),
        migrations.AlterField(
            model_name='event',
            name='free_admission',
            field=models.BooleanField(default=False, verbose_name='Free admission'),
        ),
        migrations.AlterField(
            model_name='event',
            name='press_text_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Pressetext', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='press_text_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Pressetext', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='press_text_es',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Pressetext', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='press_text_fr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Pressetext', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='press_text_it',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Pressetext', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='press_text_pl',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Pressetext', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='press_text_tr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Pressetext', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='suitable_for_children',
            field=models.BooleanField(default=False, verbose_name='Also suitable for children'),
        ),
    ]
