# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshop',
            name='admission_price_info_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='admission_price_info_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='admission_price_info_es',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='admission_price_info_fr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='admission_price_info_it',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='admission_price_info_pl',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='admission_price_info_tr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittspreis Infotext', blank=True),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='booking_info_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Anmeldung/Buchung', blank=True),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='booking_info_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Anmeldung/Buchung', blank=True),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='booking_info_es',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Anmeldung/Buchung', blank=True),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='booking_info_fr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Anmeldung/Buchung', blank=True),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='booking_info_it',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Anmeldung/Buchung', blank=True),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='booking_info_pl',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Anmeldung/Buchung', blank=True),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='booking_info_tr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Anmeldung/Buchung', blank=True),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='description_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='description_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='description_es',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='description_fr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='description_it',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='description_locked',
            field=models.BooleanField(default=False, help_text="When checked, press text won't be copied automatically to description.", verbose_name='Description locked'),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='description_pl',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='description_tr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='free_admission',
            field=models.BooleanField(default=False, verbose_name='Free admission'),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='has_group_offer',
            field=models.BooleanField(default=False, verbose_name='Has bookable group offer'),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='is_for_blind',
            field=models.BooleanField(default=False, verbose_name='Special for blind people'),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='is_for_deaf',
            field=models.BooleanField(default=False, verbose_name='Special for deaf people'),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='is_for_dementia_sufferers',
            field=models.BooleanField(default=False, verbose_name='Special for sufferers of dementia'),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='is_for_families',
            field=models.BooleanField(default=False, verbose_name='Special for families'),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='is_for_learning_difficulties',
            field=models.BooleanField(default=False, verbose_name='Special for people with learning difficulties'),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='is_for_preschool',
            field=models.BooleanField(default=False, verbose_name='Special for preschool children (up to 5 years)'),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='is_for_primary_school',
            field=models.BooleanField(default=False, verbose_name='Special for children of primary school age (6-12 years)'),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='is_for_wheelchaired',
            field=models.BooleanField(default=False, verbose_name='Special for people in wheelchairs'),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='is_for_youth',
            field=models.BooleanField(default=False, verbose_name='Special for youth (aged 13 years)'),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='press_text_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Pressetext', blank=True),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='press_text_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Pressetext', blank=True),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='press_text_es',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Pressetext', blank=True),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='press_text_fr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Pressetext', blank=True),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='press_text_it',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Pressetext', blank=True),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='press_text_pl',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Pressetext', blank=True),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='press_text_tr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Pressetext', blank=True),
        ),
    ]
