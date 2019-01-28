# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
            ],
            options={
                'ordering': ['production__title'],
                'verbose_name': 'Multipart production',
                'verbose_name_plural': 'Multipart productions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(default=0, verbose_name='Sort Order')),
                ('parent', models.ForeignKey(verbose_name='Parent', to='multiparts.Parent')),
            ],
            options={
                'ordering': ['sort_order'],
                'verbose_name': 'Part',
                'verbose_name_plural': 'Parts',
            },
            bases=(models.Model,),
        ),
    ]
