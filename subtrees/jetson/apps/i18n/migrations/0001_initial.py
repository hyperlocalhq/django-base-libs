# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('name_id', models.CharField(max_length=6, serialize=False, verbose_name='name identifier', primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='area name')),
                ('alt_name', models.CharField(max_length=50, verbose_name='area alternate name', blank=True)),
                ('abbrev', models.CharField(max_length=3, verbose_name='postal abbreviation', blank=True)),
                ('reg_area', models.CharField(blank=True, max_length=1, verbose_name='regional administrative area', choices=[(b'a', 'Another'), (b'i', 'Island'), (b'ar', 'Arrondissement'), (b'at', 'Atoll'), (b'ai', 'Autonomous island'), (b'ca', 'Canton'), (b'cm', 'Commune'), (b'co', 'County'), (b'dp', 'Department'), (b'de', 'Dependency'), (b'dt', 'District'), (b'dv', 'Division'), (b'em', 'Emirate'), (b'gv', 'Governorate'), (b'ic', 'Island council'), (b'ig', 'Island group'), (b'ir', 'Island region'), (b'kd', 'Kingdom'), (b'mu', 'Municipality'), (b'pa', 'Parish'), (b'pf', 'Prefecture'), (b'pr', 'Province'), (b'rg', 'Region'), (b'rp', 'Republic'), (b'sh', 'Sheading'), (b'st', 'State'), (b'sd', 'Subdivision'), (b'sj', 'Subject'), (b'ty', 'Territory')])),
            ],
            options={
                'ordering': ['country'],
                'verbose_name': 'area',
                'verbose_name_plural': 'areas',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('name', models.CharField(unique=True, max_length=56, verbose_name='Country Name (English)')),
                ('name_de', models.CharField(max_length=56, verbose_name='Country Name (German)', blank=True)),
                ('iso3_code', models.CharField(max_length=3, verbose_name='Alpha-3 ISO Code')),
                ('iso2_code', models.CharField(max_length=2, unique=True, serialize=False, verbose_name='Alpha-2 ISO Code', primary_key=True)),
                ('region', models.CharField(max_length=5, verbose_name='Geographical Region', choices=[(b'af.e', 'Eastern Africa'), (b'af.m', 'Middle Africa'), (b'af.n', 'Northern Africa'), (b'af.s', 'Southern Africa'), (b'af.w', 'Western Africa'), (b'am.ca', 'Caribbean'), (b'am.c', 'Central America'), (b'am.s', 'South America'), (b'am.n', 'Northern America'), (b'as.c', 'Central Asia'), (b'as.e', 'Eastern Asia'), (b'as.s', 'Southern Asia'), (b'as.se', 'South-Eastern Asia'), (b'as.w', 'Western Asia'), (b'e.e', 'Eastern Europe'), (b'e.n', 'Northern Europe'), (b'e.s', 'Southern Europe'), (b'e.w', 'Western Europe'), (b'o.a', 'Australia and New Zealand'), (b'o.me', 'Melanesia'), (b'o.mi', 'Micronesia'), (b'o.p', 'Polynesia')])),
                ('territory_of', models.CharField(max_length=3, verbose_name='Territory of', blank=True)),
                ('adm_area', models.CharField(blank=True, max_length=2, verbose_name='Administrative Area', choices=[(b'a', 'Another'), (b'i', 'Island'), (b'ar', 'Arrondissement'), (b'at', 'Atoll'), (b'ai', 'Autonomous island'), (b'ca', 'Canton'), (b'cm', 'Commune'), (b'co', 'County'), (b'dp', 'Department'), (b'de', 'Dependency'), (b'dt', 'District'), (b'dv', 'Division'), (b'em', 'Emirate'), (b'gv', 'Governorate'), (b'ic', 'Island council'), (b'ig', 'Island group'), (b'ir', 'Island region'), (b'kd', 'Kingdom'), (b'mu', 'Municipality'), (b'pa', 'Parish'), (b'pf', 'Prefecture'), (b'pr', 'Province'), (b'rg', 'Region'), (b'rp', 'Republic'), (b'sh', 'Sheading'), (b'st', 'State'), (b'sd', 'Subdivision'), (b'sj', 'Subject'), (b'ty', 'Territory')])),
                ('display', models.BooleanField(default=True, help_text='Designates whether the country is shown.', verbose_name='Display')),
                ('sort_order', models.PositiveIntegerField(default=20, verbose_name='Sort Order')),
            ],
            options={
                'ordering': ['sort_order', 'name'],
                'verbose_name': 'country',
                'verbose_name_plural': 'countries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CountryLanguage',
            fields=[
                ('lang_type', models.CharField(blank=True, max_length=1, verbose_name='language type', choices=[(b'o', 'official'), (b'n', 'national'), (b'r', 'regional'), (b'f', 'de facto'), (b'j', 'de jure'), (b'l', 'legislative'), (b'b', 'business')])),
                ('identifier', models.CharField(max_length=6, serialize=False, verbose_name='identifier', primary_key=True)),
                ('country', models.ForeignKey(to='i18n.Country')),
            ],
            options={
                'ordering': ['country'],
                'verbose_name': 'country & language',
                'verbose_name_plural': 'countries & languages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('iso3_code', models.CharField(max_length=3, verbose_name='Alpha-3 ISO Code')),
                ('name', models.CharField(unique=True, max_length=40, verbose_name='Language Name (English)')),
                ('name_de', models.CharField(max_length=40, verbose_name='Language Name (German)', blank=True)),
                ('iso2_code', models.CharField(max_length=2, verbose_name='Alpha-2 ISO Code', blank=True)),
                ('synonym', models.CharField(max_length=40, verbose_name='Language Synonym', blank=True)),
                ('display', models.BooleanField(default=False, help_text='Designates whether the language is shown.', verbose_name='Display')),
                ('sort_order', models.PositiveIntegerField(default=20, verbose_name='Sort order')),
            ],
            options={
                'ordering': ['sort_order', 'name'],
                'verbose_name': 'language',
                'verbose_name_plural': 'languages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Nationality',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=40, verbose_name='Nationality Name (English)')),
                ('name_de', models.CharField(max_length=40, verbose_name='Nationality Name (German)', blank=True)),
                ('display', models.BooleanField(default=False, help_text='Designates whether the language is shown.', verbose_name='Display')),
                ('sort_order', models.PositiveIntegerField(default=20, verbose_name='Sort order')),
            ],
            options={
                'ordering': ['sort_order', 'name'],
                'verbose_name': 'nationality',
                'verbose_name_plural': 'nationalities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.PositiveSmallIntegerField(null=True, verbose_name='country code', blank=True)),
                ('ln_area', models.CharField(max_length=10, verbose_name='length of area code', blank=True)),
                ('ln_sn', models.CharField(max_length=8, verbose_name='length of subscriber number (SN)', blank=True)),
                ('ln_area_sn', models.CharField(max_length=8, verbose_name='length of area code and SN', blank=True)),
                ('nat_prefix', models.CharField(max_length=2, verbose_name='national prefix', blank=True)),
                ('int_prefix', models.CharField(max_length=4, verbose_name='international prefix', blank=True)),
                ('country', models.ForeignKey(to='i18n.Country')),
            ],
            options={
                'ordering': ['country'],
                'verbose_name': 'phone',
                'verbose_name_plural': 'phones',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TimeZone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('zone', models.CharField(unique=True, max_length=32, verbose_name='time zone')),
                ('country', models.ForeignKey(to='i18n.Country')),
            ],
            options={
                'ordering': ['zone'],
                'verbose_name': 'time zone',
                'verbose_name_plural': 'time zones',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='countrylanguage',
            name='language',
            field=models.ForeignKey(to='i18n.Language'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='area',
            name='country',
            field=models.ForeignKey(to='i18n.Country'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='area',
            unique_together=set([('country', 'name')]),
        ),
    ]
