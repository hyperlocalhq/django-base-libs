# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_mods', '0004_longer_original_path_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagemodification',
            name='filters',
            field=models.CharField(help_text='W\xe4hlen Sie mehrere Filter mit dem folgenden Muster "FILTER_EINS->FILTER_ZWEI->FILTER_DREI". Image Filter werden in der Reihenfolge angewendet. Die folgenden Filter stehen zur Verf\xfcgung: BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE, EMBOSS, FIND_EDGES, SHARPEN, SMOOTH, SMOOTH_MORE', max_length=200, verbose_name='Filters', blank=True),
        ),
    ]
