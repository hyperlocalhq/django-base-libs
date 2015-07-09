# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jetson.apps.optionset.models


class Migration(migrations.Migration):

    dependencies = [
        ('optionset', '__first__'),
        ('location', '__first__'),
        ('events', '0002_event_organizing_institution'),
        ('people', '0001_initial'),
        ('institutions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='organizing_person',
            field=models.ForeignKey(related_name='events_organized', verbose_name='Organizing person', blank=True, to='people.Person', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='phone0_type',
            field=models.ForeignKey(related_name='events0', default=jetson.apps.optionset.models.get_default_phonetype_for_phone, blank=True, to='optionset.PhoneType', null=True, verbose_name='Phone Type'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='phone1_type',
            field=models.ForeignKey(related_name='events1', default=jetson.apps.optionset.models.get_default_phonetype_for_fax, blank=True, to='optionset.PhoneType', null=True, verbose_name='Phone Type'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='phone2_type',
            field=models.ForeignKey(related_name='events2', default=jetson.apps.optionset.models.get_default_phonetype_for_mobile, blank=True, to='optionset.PhoneType', null=True, verbose_name='Phone Type'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='postal_address',
            field=models.ForeignKey(related_name='address_events', verbose_name='Postal Address', blank=True, to='location.Address', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='related_events',
            field=models.ManyToManyField(related_name='related_events_rel_+', to='events.Event', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='url0_type',
            field=models.ForeignKey(related_name='events0', verbose_name='URL Type', blank=True, to='optionset.URLType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='url1_type',
            field=models.ForeignKey(related_name='events1', verbose_name='URL Type', blank=True, to='optionset.URLType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='url2_type',
            field=models.ForeignKey(related_name='events2', verbose_name='URL Type', blank=True, to='optionset.URLType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='venue',
            field=models.ForeignKey(related_name='events_happened', verbose_name='Venue', blank=True, to='institutions.Institution', null=True),
            preserve_default=True,
        ),
    ]
