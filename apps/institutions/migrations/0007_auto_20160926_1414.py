# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0006_auto_20160901_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institutionalcontact',
            name='email0_type',
            field=models.ForeignKey(related_name='institutional_contacts0', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Email Type', blank=True, to='optionset.EmailType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='institutionalcontact',
            name='email1_type',
            field=models.ForeignKey(related_name='institutional_contacts1', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Email Type', blank=True, to='optionset.EmailType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='institutionalcontact',
            name='email2_type',
            field=models.ForeignKey(related_name='institutional_contacts2', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Email Type', blank=True, to='optionset.EmailType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='institutionalcontact',
            name='im0_type',
            field=models.ForeignKey(related_name='institutional_contacts0', on_delete=django.db.models.deletion.SET_NULL, verbose_name='IM Type', blank=True, to='optionset.IMType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='institutionalcontact',
            name='im1_type',
            field=models.ForeignKey(related_name='institutional_contacts1', on_delete=django.db.models.deletion.SET_NULL, verbose_name='IM Type', blank=True, to='optionset.IMType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='institutionalcontact',
            name='im2_type',
            field=models.ForeignKey(related_name='institutional_contacts2', on_delete=django.db.models.deletion.SET_NULL, verbose_name='IM Type', blank=True, to='optionset.IMType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='institutionalcontact',
            name='url0_type',
            field=models.ForeignKey(related_name='institutional_contacts0', on_delete=django.db.models.deletion.SET_NULL, verbose_name='URL Type', blank=True, to='optionset.URLType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='institutionalcontact',
            name='url1_type',
            field=models.ForeignKey(related_name='institutional_contacts1', on_delete=django.db.models.deletion.SET_NULL, verbose_name='URL Type', blank=True, to='optionset.URLType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='institutionalcontact',
            name='url2_type',
            field=models.ForeignKey(related_name='institutional_contacts2', on_delete=django.db.models.deletion.SET_NULL, verbose_name='URL Type', blank=True, to='optionset.URLType', null=True),
            preserve_default=True,
        ),
    ]
