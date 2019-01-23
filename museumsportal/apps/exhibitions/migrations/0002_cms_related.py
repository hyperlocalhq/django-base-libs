# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exhibitions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewlyOpenedExhibition',
            fields=[
                ('cmsplugin_ptr',
                 models.OneToOneField(parent_link=True, related_name='exhibitions_newlyopenedexhibition',
                                      auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('exhibition', models.ForeignKey(to='exhibitions.Exhibition')),
            ],
            options={
                'ordering': ['exhibition__title'],
                'verbose_name': 'Newly opened exhibition',
                'verbose_name_plural': 'Newly opened exhibitions',
            },
            bases=('cms.cmsplugin',),
        ),
    ]
