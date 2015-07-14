# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import jetson.apps.optionset.models


class Migration(migrations.Migration):

    dependencies = [
        ('optionset', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('marketplace', '0001_initial'),
        ('institutions', '0001_initial'),
        ('location', '0001_initial'),
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='joboffer',
            name='contact_person',
            field=models.ForeignKey(related_name='jobs_posted', verbose_name='Organizing person', blank=True, to='people.Person', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='joboffer',
            name='creator',
            field=models.ForeignKey(related_name='joboffer_creator', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='creator'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='joboffer',
            name='email0_type',
            field=models.ForeignKey(related_name='job_offers0', verbose_name='Email Type', blank=True, to='optionset.EmailType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='joboffer',
            name='email1_type',
            field=models.ForeignKey(related_name='job_offers1', verbose_name='Email Type', blank=True, to='optionset.EmailType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='joboffer',
            name='email2_type',
            field=models.ForeignKey(related_name='job_offers2', verbose_name='Email Type', blank=True, to='optionset.EmailType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='joboffer',
            name='im0_type',
            field=models.ForeignKey(related_name='job_offers0', verbose_name='IM Type', blank=True, to='optionset.IMType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='joboffer',
            name='im1_type',
            field=models.ForeignKey(related_name='job_offers1', verbose_name='IM Type', blank=True, to='optionset.IMType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='joboffer',
            name='im2_type',
            field=models.ForeignKey(related_name='job_offers2', verbose_name='IM Type', blank=True, to='optionset.IMType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='joboffer',
            name='job_sectors',
            field=models.ManyToManyField(related_name='job_sector_joboffers', verbose_name='Job sectors', to='marketplace.JobSector', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='joboffer',
            name='job_type',
            field=models.ForeignKey(verbose_name='Job type', to='marketplace.JobType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='joboffer',
            name='modifier',
            field=models.ForeignKey(related_name='joboffer_modifier', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modifier'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='joboffer',
            name='offering_institution',
            field=models.ForeignKey(verbose_name='Organizing institution', blank=True, to='institutions.Institution', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='joboffer',
            name='phone0_type',
            field=models.ForeignKey(related_name='job_offers0', default=jetson.apps.optionset.models.get_default_phonetype_for_phone, blank=True, to='optionset.PhoneType', null=True, verbose_name='Phone Type'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='joboffer',
            name='phone1_type',
            field=models.ForeignKey(related_name='job_offers1', default=jetson.apps.optionset.models.get_default_phonetype_for_fax, blank=True, to='optionset.PhoneType', null=True, verbose_name='Phone Type'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='joboffer',
            name='phone2_type',
            field=models.ForeignKey(related_name='job_offers2', default=jetson.apps.optionset.models.get_default_phonetype_for_mobile, blank=True, to='optionset.PhoneType', null=True, verbose_name='Phone Type'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='joboffer',
            name='postal_address',
            field=models.ForeignKey(related_name='address_job_offers', verbose_name='Postal Address', blank=True, to='location.Address', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='joboffer',
            name='qualifications',
            field=models.ManyToManyField(related_name='joboffers', verbose_name='Qualifications', to='marketplace.JobQualification', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='joboffer',
            name='url0_type',
            field=models.ForeignKey(related_name='job_offers0', verbose_name='URL Type', blank=True, to='optionset.URLType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='joboffer',
            name='url1_type',
            field=models.ForeignKey(related_name='job_offers1', verbose_name='URL Type', blank=True, to='optionset.URLType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='joboffer',
            name='url2_type',
            field=models.ForeignKey(related_name='job_offers2', verbose_name='URL Type', blank=True, to='optionset.URLType', null=True),
            preserve_default=True,
        ),
    ]
