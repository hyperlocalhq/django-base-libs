# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import filebrowser.fields
from django.utils.timezone import utc
import django.utils.timezone
import django.db.models.deletion
from django.conf import settings
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdBase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('url', models.URLField(verbose_name='Advertised URL')),
                ('language', models.CharField(default=b'', max_length=5, verbose_name='Language', blank=True, choices=[('de', 'Deutsch'), ('en', 'English'), ('fr', 'Fran\xe7ais'), ('pl', 'Polski'), ('tr', 'T\xfcrk\xe7e'), ('es', 'Espa\xf1ol'), ('it', 'Italiano')])),
                ('start_showing', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Start showing')),
                ('stop_showing', models.DateTimeField(default=datetime.datetime(9999, 12, 29, 23, 59, 59, 999999, tzinfo=utc), verbose_name='Stop showing')),
                ('show_ad_label', models.BooleanField(default=True, verbose_name='Show label "Advertisement"')),
                ('impressions_stats', models.TextField(verbose_name='Impressions', editable=False, blank=True)),
                ('clicks_stats', models.TextField(verbose_name='CLicks', editable=False, blank=True)),
            ],
            options={
                'verbose_name': 'Ad Base',
                'verbose_name_plural': 'Ad Bases',
            },
        ),
        migrations.CreateModel(
            name='AdCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sysname', models.SlugField(help_text='Do not change this value!', unique=True, max_length=255, verbose_name='Sysname')),
                ('title', models.CharField(verbose_name='Title', max_length=255, null=True, editable=False)),
                ('description', models.TextField(default=b'', verbose_name='Description', null=True, editable=False, blank=True)),
                ('description_de', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Description', blank=True)),
                ('description_de_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('description_en', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Description', blank=True)),
                ('description_en_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('description_fr', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Description', blank=True)),
                ('description_fr_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('description_pl', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Description', blank=True)),
                ('description_pl_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('description_tr', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Description', blank=True)),
                ('description_tr_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('description_es', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Description', blank=True)),
                ('description_es_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('description_it', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Description', blank=True)),
                ('description_it_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('title_de', models.CharField(max_length=255, verbose_name='Title')),
                ('title_en', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_fr', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_pl', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_tr', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_es', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_it', models.CharField(max_length=255, verbose_name='Title', blank=True)),
            ],
            options={
                'ordering': ('title',),
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='AdClick',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('click_date', models.DateTimeField(auto_now_add=True, verbose_name='When')),
                ('source_ip', models.GenericIPAddressField(null=True, verbose_name='Who', blank=True)),
            ],
            options={
                'verbose_name': 'Ad Click',
                'verbose_name_plural': 'Ad Clicks',
            },
        ),
        migrations.CreateModel(
            name='AdImpression',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('impression_date', models.DateTimeField(auto_now_add=True, verbose_name='When')),
                ('source_ip', models.GenericIPAddressField(null=True, verbose_name='Who', blank=True)),
            ],
            options={
                'verbose_name': 'Ad Impression',
                'verbose_name_plural': 'Ad Impressions',
            },
        ),
        migrations.CreateModel(
            name='Advertiser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company_name', models.CharField(max_length=255, verbose_name='Company Name')),
                ('website', models.URLField(verbose_name='Company Site', blank=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('company_name',),
                'verbose_name': 'Ad Provider',
                'verbose_name_plural': 'Advertisers',
            },
        ),
        migrations.CreateModel(
            name='AdZone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sysname', models.SlugField(help_text='Do not change this value!', unique=True, max_length=255, verbose_name='Sysname')),
                ('title', models.CharField(verbose_name='Title', max_length=255, null=True, editable=False)),
                ('description', models.TextField(default=b'', verbose_name='Description', null=True, editable=False, blank=True)),
                ('description_de', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Description', blank=True)),
                ('description_de_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('description_en', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Description', blank=True)),
                ('description_en_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('description_fr', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Description', blank=True)),
                ('description_fr_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('description_pl', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Description', blank=True)),
                ('description_pl_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('description_tr', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Description', blank=True)),
                ('description_tr_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('description_es', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Description', blank=True)),
                ('description_es_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('description_it', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Description', blank=True)),
                ('description_it_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('title_de', models.CharField(max_length=255, verbose_name='Title')),
                ('title_en', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_fr', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_pl', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_tr', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_es', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_it', models.CharField(max_length=255, verbose_name='Title', blank=True)),
            ],
            options={
                'ordering': ('title',),
                'verbose_name': 'Zone',
                'verbose_name_plural': 'Zones',
            },
        ),
        migrations.CreateModel(
            name='BannerAd',
            fields=[
                ('adbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='advertising.AdBase')),
                ('content', filebrowser.fields.FileBrowseField(max_length=255, verbose_name='Banner')),
            ],
            options={
                'abstract': False,
            },
            bases=('advertising.adbase',),
        ),
        migrations.CreateModel(
            name='TextAd',
            fields=[
                ('adbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='advertising.AdBase')),
                ('content', models.TextField(verbose_name='Content')),
            ],
            options={
                'abstract': False,
            },
            bases=('advertising.adbase',),
        ),
        migrations.AddField(
            model_name='adimpression',
            name='ad',
            field=models.ForeignKey(to='advertising.AdBase'),
        ),
        migrations.AddField(
            model_name='adclick',
            name='ad',
            field=models.ForeignKey(to='advertising.AdBase'),
        ),
        migrations.AddField(
            model_name='adbase',
            name='advertiser',
            field=models.ForeignKey(verbose_name='Ad Provider', to='advertising.Advertiser'),
        ),
        migrations.AddField(
            model_name='adbase',
            name='category',
            field=models.ForeignKey(verbose_name='Category', blank=True, to='advertising.AdCategory', null=True),
        ),
        migrations.AddField(
            model_name='adbase',
            name='creator',
            field=models.ForeignKey(related_name='adbase_creator', on_delete=django.db.models.deletion.SET_NULL, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='creator'),
        ),
        migrations.AddField(
            model_name='adbase',
            name='modifier',
            field=models.ForeignKey(related_name='adbase_modifier', on_delete=django.db.models.deletion.SET_NULL, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modifier'),
        ),
        migrations.AddField(
            model_name='adbase',
            name='zone',
            field=models.ForeignKey(verbose_name='Zone', to='advertising.AdZone'),
        ),
    ]
