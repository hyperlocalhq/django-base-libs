# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_mods', '0005_auto_20180619_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagemodification',
            name='filters',
            field=models.CharField(help_text='Chain multiple filters using the following pattern "FILTER_ONE->FILTER_TWO->FILTER_THREE". Image filters will be applied in order. The following filter are available: BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE, EMBOSS, FIND_EDGES, SHARPEN, SMOOTH, SMOOTH_MORE', max_length=200, verbose_name='Filters', blank=True),
        ),
    ]
