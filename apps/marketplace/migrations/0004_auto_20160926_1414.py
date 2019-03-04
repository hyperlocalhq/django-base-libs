# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0003_auto_20160606_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joboffer',
            name='email0_type',
            field=models.ForeignKey(related_name='job_offers0', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Email Type', blank=True, to='optionset.EmailType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='joboffer',
            name='email1_type',
            field=models.ForeignKey(related_name='job_offers1', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Email Type', blank=True, to='optionset.EmailType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='joboffer',
            name='email2_type',
            field=models.ForeignKey(related_name='job_offers2', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Email Type', blank=True, to='optionset.EmailType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='joboffer',
            name='im0_type',
            field=models.ForeignKey(related_name='job_offers0', on_delete=django.db.models.deletion.SET_NULL, verbose_name='IM Type', blank=True, to='optionset.IMType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='joboffer',
            name='im1_type',
            field=models.ForeignKey(related_name='job_offers1', on_delete=django.db.models.deletion.SET_NULL, verbose_name='IM Type', blank=True, to='optionset.IMType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='joboffer',
            name='im2_type',
            field=models.ForeignKey(related_name='job_offers2', on_delete=django.db.models.deletion.SET_NULL, verbose_name='IM Type', blank=True, to='optionset.IMType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='joboffer',
            name='url0_type',
            field=models.ForeignKey(related_name='job_offers0', on_delete=django.db.models.deletion.SET_NULL, verbose_name='URL Type', blank=True, to='optionset.URLType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='joboffer',
            name='url1_type',
            field=models.ForeignKey(related_name='job_offers1', on_delete=django.db.models.deletion.SET_NULL, verbose_name='URL Type', blank=True, to='optionset.URLType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='joboffer',
            name='url2_type',
            field=models.ForeignKey(related_name='job_offers2', on_delete=django.db.models.deletion.SET_NULL, verbose_name='URL Type', blank=True, to='optionset.URLType', null=True),
            preserve_default=True,
        ),
    ]
