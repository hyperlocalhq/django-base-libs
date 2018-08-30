# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
        ('advertising', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CMSAdZone',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='cms_ads_cmsadzone', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('category', models.ForeignKey(verbose_name='Kategorie', blank=True, to='advertising.AdCategory', null=True)),
                ('zone', models.ForeignKey(verbose_name='Zone', to='advertising.AdZone')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
