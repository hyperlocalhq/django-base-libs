# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
        ('exhibitions', '0002_cms_related'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewlyOpenedExhibitionExt',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='exhibitions_plugins_newlyopenedexhibitionext', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('teaser_text', base_libs.models.fields.ExtendedTextField(verbose_name='Teaser', blank=True)),
                ('teaser_text_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('exhibition', models.ForeignKey(to='exhibitions.Exhibition')),
            ],
            options={
                'ordering': ['exhibition__title'],
                'verbose_name': 'Newly opened exhibition with teaser',
                'verbose_name_plural': 'Newly opened exhibitions with teasers',
            },
            bases=('cms.cmsplugin',),
        ),
    ]
