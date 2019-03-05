# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImageCropping',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('original', filebrowser.fields.FileBrowseField(max_length=255, verbose_name='Original')),
                ('x1', models.IntegerField(default=0, verbose_name='X1')),
                ('y1', models.IntegerField(default=0, verbose_name='Y1')),
                ('x2', models.IntegerField(default=0, verbose_name='X2')),
                ('y2', models.IntegerField(default=0, verbose_name='Y2')),
                ('bgcolor', models.CharField(default=b'#ffffff', max_length=7, verbose_name='Canvas color')),
            ],
            options={
                'ordering': ('original',),
                'verbose_name': 'Image Cropping',
                'verbose_name_plural': 'Image Croppings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImageModification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sysname', models.SlugField(help_text='Sysnames are used for cached file suffixes and in the templates', max_length=255, verbose_name='Sysname')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('width', models.PositiveIntegerField(default=0, help_text='Leave to size the image to the set height', verbose_name='Width')),
                ('height', models.PositiveIntegerField(default=0, help_text='Leave to size the image to the set width', verbose_name='Height')),
                ('quality', models.PositiveIntegerField(default=70, help_text='JPEG image quality.', verbose_name='Quality', choices=[(30, 'Very Low'), (40, 'Low'), (50, 'Medium-Low'), (60, 'Medium'), (70, 'Medium-High'), (80, 'High'), (90, 'Very High')])),
                ('crop', models.BooleanField(default=False, help_text='If selected the image will be scaled and cropped to fit the supplied dimensions.', verbose_name='Crop to fit?')),
                ('crop_from', models.CharField(default=b'center', max_length=10, verbose_name='Crop from', blank=True, choices=[(b'top', 'Top'), (b'right', 'Right'), (b'bottom', 'Bottom'), (b'left', 'Left'), (b'center', 'Center (Default)')])),
                ('mask', filebrowser.fields.FileBrowseField(max_length=255, null=True, verbose_name='Mask', blank=True)),
                ('frame', filebrowser.fields.FileBrowseField(max_length=255, null=True, verbose_name='Frame', blank=True)),
                ('output_format', models.CharField(default=b'png', max_length=255, verbose_name='Output format', choices=[(b'png', b'PNG'), (b'jpg', b'JPEG'), (b'gif', b'GIF')])),
                ('color', models.FloatField(default=1.0, help_text='A factor of 0.0 gives a black and white image, a factor of 1.0 gives the original image.', verbose_name='Color')),
                ('brightness', models.FloatField(default=1.0, help_text='A factor of 0.0 gives a black image, a factor of 1.0 gives the original image.', verbose_name='Brightness')),
                ('contrast', models.FloatField(default=1.0, help_text='A factor of 0.0 gives a solid grey image, a factor of 1.0 gives the original image.', verbose_name='Contrast')),
                ('sharpness', models.FloatField(default=1.0, help_text='A factor of 0.0 gives a blurred image, a factor of 1.0 gives the original image.', verbose_name='Sharpness')),
                ('filters', models.CharField(help_text='W\xe4hlen Sie mehrere Filter mit dem folgenden Muster "FILTER_EINS->FILTER_ZWEI->FILTER_DREI". Image Filter werden in der Reihenfolge angewendet. Die folgenden Filter stehen zur Verf\xfcgung: BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE, EMBOSS, FIND_EDGES, SHARPEN, SMOOTH, SMOOTH_MORE', max_length=200, verbose_name='Filters', blank=True)),
            ],
            options={
                'ordering': ('sysname',),
                'verbose_name': 'Image Modification',
                'verbose_name_plural': 'Image Modifications',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImageModificationGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
            ],
            options={
                'ordering': ('title',),
                'verbose_name': 'Image Modification Group',
                'verbose_name_plural': 'Image Modification Groups',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='imagemodification',
            name='group',
            field=models.ForeignKey(blank=True, to='image_mods.ImageModificationGroup', help_text='Assign a group of modifications which will be triggered together while cropping.', null=True, verbose_name='Image Modification Group'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='imagecropping',
            name='mods',
            field=models.ManyToManyField(help_text='Modifications with the same ratio which should be used to recrop images together.', to='image_mods.ImageModification', verbose_name='Modifications'),
            preserve_default=True,
        ),
    ]
