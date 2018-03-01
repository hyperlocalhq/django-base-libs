# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HttpState',
            fields=[
                ('httpstate_key', models.CharField(max_length=40, serialize=False, verbose_name='httpstate key', primary_key=True)),
                ('httpstate_data', models.TextField(verbose_name='httpstate data')),
                ('expire_date', models.DateTimeField(verbose_name='expire date')),
            ],
            options={
                'verbose_name': 'httpstate',
                'verbose_name_plural': 'httpstates',
            },
            bases=(models.Model,),
        ),
    ]
