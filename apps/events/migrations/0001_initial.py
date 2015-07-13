# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import filebrowser.fields
from django.conf import settings
import base_libs.models.fields
import tagging_autocomplete.models


class Migration(migrations.Migration):

    dependencies = [
        ('optionset', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('structure', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('is_appointment_based', models.BooleanField(default=False, verbose_name='Visiting by Appointment')),
                ('mon_open', models.TimeField(null=True, verbose_name='Opens on Monday', blank=True)),
                ('mon_break_close', models.TimeField(null=True, verbose_name='Break Starts on Monday', blank=True)),
                ('mon_break_open', models.TimeField(null=True, verbose_name='Break Ends on Monday', blank=True)),
                ('mon_close', models.TimeField(null=True, verbose_name='Closes on Monday', blank=True)),
                ('tue_open', models.TimeField(null=True, verbose_name='Opens on Tuesday', blank=True)),
                ('tue_break_close', models.TimeField(null=True, verbose_name='Break Starts on Tuesday', blank=True)),
                ('tue_break_open', models.TimeField(null=True, verbose_name='Break Ends on Tuesday', blank=True)),
                ('tue_close', models.TimeField(null=True, verbose_name='Closes on Tuesday', blank=True)),
                ('wed_open', models.TimeField(null=True, verbose_name='Opens on Wednesday', blank=True)),
                ('wed_break_close', models.TimeField(null=True, verbose_name='Break Starts on Wednesday', blank=True)),
                ('wed_break_open', models.TimeField(null=True, verbose_name='Break Ends on Wednesday', blank=True)),
                ('wed_close', models.TimeField(null=True, verbose_name='Closes on Wednesday', blank=True)),
                ('thu_open', models.TimeField(null=True, verbose_name='Opens on Thursday', blank=True)),
                ('thu_break_close', models.TimeField(null=True, verbose_name='Break Starts on Thursday', blank=True)),
                ('thu_break_open', models.TimeField(null=True, verbose_name='Break Ends on Thursday', blank=True)),
                ('thu_close', models.TimeField(null=True, verbose_name='Closes on Thursday', blank=True)),
                ('fri_open', models.TimeField(null=True, verbose_name='Opens on Friday', blank=True)),
                ('fri_break_close', models.TimeField(null=True, verbose_name='Break Starts on Friday', blank=True)),
                ('fri_break_open', models.TimeField(null=True, verbose_name='Break Ends on Friday', blank=True)),
                ('fri_close', models.TimeField(null=True, verbose_name='Closes on Friday', blank=True)),
                ('sat_open', models.TimeField(null=True, verbose_name='Opens on Saturday', blank=True)),
                ('sat_break_close', models.TimeField(null=True, verbose_name='Break Starts on Saturday', blank=True)),
                ('sat_break_open', models.TimeField(null=True, verbose_name='Break Ends on Saturday', blank=True)),
                ('sat_close', models.TimeField(null=True, verbose_name='Closes on Saturday', blank=True)),
                ('sun_open', models.TimeField(null=True, verbose_name='Opens on Sunday', blank=True)),
                ('sun_break_close', models.TimeField(null=True, verbose_name='Break Starts on Sunday', blank=True)),
                ('sun_break_open', models.TimeField(null=True, verbose_name='Break Ends on Sunday', blank=True)),
                ('sun_close', models.TimeField(null=True, verbose_name='Closes on Sunday', blank=True)),
                ('exceptions', base_libs.models.fields.MultilingualTextField(default=b'', verbose_name='Exceptions for working hours', null=True, editable=False, blank=True)),
                ('title', base_libs.models.fields.MultilingualCharField(verbose_name='Title', max_length=255, null=True, editable=False)),
                ('slug', models.CharField(max_length=255, verbose_name='Slug for URIs')),
                ('description', base_libs.models.fields.MultilingualTextField(default=b'', verbose_name='Description', null=True, editable=False, blank=True)),
                ('image', filebrowser.fields.FileBrowseField(max_length=200, verbose_name='Image', blank=True)),
                ('start', models.DateTimeField(verbose_name='Start', null=True, editable=False, blank=True)),
                ('end', models.DateTimeField(verbose_name='End', null=True, editable=False, blank=True)),
                ('status', models.CharField(default=b'draft', max_length=20, verbose_name='Status', blank=True, choices=[(b'draft', 'Draft'), (b'published', 'Published'), (b'not_listed', 'Not Listed'), (b'import', 'Imported'), (b'expired', 'Expired')])),
                ('venue_title', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('organizer_title', models.TextField(null=True, verbose_name='Organizer', blank=True)),
                ('organizer_url_link', base_libs.models.fields.URLField(null=True, verbose_name='Organizer URL', blank=True)),
                ('additional_info', base_libs.models.fields.MultilingualTextField(default=b'', verbose_name='Additional Info', null=True, editable=False, blank=True)),
                ('phone0_country', models.CharField(default=b'49', max_length=4, verbose_name='Country Code', blank=True)),
                ('phone0_area', models.CharField(default=b'30', max_length=6, verbose_name='Area Code', blank=True)),
                ('phone0_number', models.CharField(max_length=25, verbose_name='Subscriber Number and Extension', blank=True)),
                ('is_phone0_default', models.BooleanField(default=True, verbose_name='Default?')),
                ('is_phone0_on_hold', models.BooleanField(default=False, verbose_name='On Hold?')),
                ('phone1_country', models.CharField(default=b'49', max_length=4, verbose_name='Country Code', blank=True)),
                ('phone1_area', models.CharField(default=b'30', max_length=6, verbose_name='Area Code', blank=True)),
                ('phone1_number', models.CharField(max_length=25, verbose_name='Subscriber Number and Extension', blank=True)),
                ('is_phone1_default', models.BooleanField(default=False, verbose_name='Default?')),
                ('is_phone1_on_hold', models.BooleanField(default=False, verbose_name='On Hold?')),
                ('phone2_country', models.CharField(default=b'49', max_length=4, verbose_name='Country Code', blank=True)),
                ('phone2_area', models.CharField(max_length=6, verbose_name='Area Code', blank=True)),
                ('phone2_number', models.CharField(max_length=25, verbose_name='Subscriber Number and Extension', blank=True)),
                ('is_phone2_default', models.BooleanField(default=False, verbose_name='Default?')),
                ('is_phone2_on_hold', models.BooleanField(default=False, verbose_name='On Hold?')),
                ('url0_link', base_libs.models.fields.URLField(verbose_name='URL', blank=True)),
                ('is_url0_default', models.BooleanField(default=True, verbose_name='Default?')),
                ('is_url0_on_hold', models.BooleanField(default=False, verbose_name='On Hold?')),
                ('url1_link', base_libs.models.fields.URLField(verbose_name='URL', blank=True)),
                ('is_url1_default', models.BooleanField(default=False, verbose_name='Default?')),
                ('is_url1_on_hold', models.BooleanField(default=False, verbose_name='On Hold?')),
                ('url2_link', base_libs.models.fields.URLField(verbose_name='URL', blank=True)),
                ('is_url2_default', models.BooleanField(default=False, verbose_name='Default?')),
                ('is_url2_on_hold', models.BooleanField(default=False, verbose_name='On Hold?')),
                ('im0_address', models.CharField(max_length=255, verbose_name='Instant Messenger', blank=True)),
                ('is_im0_default', models.BooleanField(default=True, verbose_name='Default?')),
                ('is_im0_on_hold', models.BooleanField(default=False, verbose_name='On Hold?')),
                ('im1_address', models.CharField(max_length=255, verbose_name='Instant Messenger', blank=True)),
                ('is_im1_default', models.BooleanField(default=False, verbose_name='Default?')),
                ('is_im1_on_hold', models.BooleanField(default=False, verbose_name='On Hold?')),
                ('im2_address', models.CharField(max_length=255, verbose_name='Instant Messenger', blank=True)),
                ('is_im2_default', models.BooleanField(default=False, verbose_name='Default?')),
                ('is_im2_on_hold', models.BooleanField(default=False, verbose_name='On Hold?')),
                ('email0_address', models.CharField(max_length=255, verbose_name='Email Address', blank=True)),
                ('is_email0_default', models.BooleanField(default=True, verbose_name='Default?')),
                ('is_email0_on_hold', models.BooleanField(default=False, verbose_name='On Hold?')),
                ('email1_address', models.CharField(max_length=255, verbose_name='Email Address', blank=True)),
                ('is_email1_default', models.BooleanField(default=False, verbose_name='Default?')),
                ('is_email1_on_hold', models.BooleanField(default=False, verbose_name='On Hold?')),
                ('email2_address', models.CharField(max_length=255, verbose_name='Email Address', blank=True)),
                ('is_email2_default', models.BooleanField(default=False, verbose_name='Default?')),
                ('is_email2_on_hold', models.BooleanField(default=False, verbose_name='On Hold?')),
                ('tags', tagging_autocomplete.models.TagAutocompleteField(default=b'', help_text='Separate different tags by comma', max_length=255, verbose_name='tags', blank=True)),
                ('fees', base_libs.models.fields.MultilingualTextField(default=b'', verbose_name='Fees', null=True, editable=False, blank=True)),
                ('is_featured', models.BooleanField(default=False, verbose_name='Featured')),
                ('importance', models.IntegerField(default=0, verbose_name='Importance')),
                ('fees_de', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittskosten', blank=True)),
                ('fees_de_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('fees_en', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Eintrittskosten', blank=True)),
                ('fees_en_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('exceptions_de', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Sonstige \xd6ffnungszeiten', blank=True)),
                ('exceptions_de_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('exceptions_en', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Sonstige \xd6ffnungszeiten', blank=True)),
                ('exceptions_en_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('title_de', models.CharField(max_length=255, verbose_name='Title')),
                ('title_en', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('description_de', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True)),
                ('description_de_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('description_en', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True)),
                ('description_en_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('additional_info_de', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Zusatzinformation', blank=True)),
                ('additional_info_de_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('additional_info_en', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Zusatzinformation', blank=True)),
                ('additional_info_en_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('creative_sectors', mptt.fields.TreeManyToManyField(related_name='creative_industry_events', verbose_name='Creative sectors', to='structure.Term', blank=True)),
                ('creator', models.ForeignKey(related_name='event_creator', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='creator')),
                ('email0_type', models.ForeignKey(related_name='events0', verbose_name='Email Type', blank=True, to='optionset.EmailType', null=True)),
                ('email1_type', models.ForeignKey(related_name='events1', verbose_name='Email Type', blank=True, to='optionset.EmailType', null=True)),
                ('email2_type', models.ForeignKey(related_name='events2', verbose_name='Email Type', blank=True, to='optionset.EmailType', null=True)),
            ],
            options={
                'ordering': ['title', 'creation_date'],
                'abstract': False,
                'verbose_name': 'event',
                'verbose_name_plural': 'events',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_yyyy', models.IntegerField(default=2015, verbose_name='Start Year', choices=[(1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024)])),
                ('start_mm', models.SmallIntegerField(blank=True, null=True, verbose_name='Start Month', choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')])),
                ('start_dd', models.SmallIntegerField(blank=True, null=True, verbose_name='Start Day', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31)])),
                ('start_hh', models.SmallIntegerField(blank=True, null=True, verbose_name='Start Hour', choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23)])),
                ('start_ii', models.SmallIntegerField(blank=True, null=True, verbose_name='Start Minute', choices=[(0, b'00'), (1, b'01'), (2, b'02'), (3, b'03'), (4, b'04'), (5, b'05'), (6, b'06'), (7, b'07'), (8, b'08'), (9, b'09'), (10, b'10'), (11, b'11'), (12, b'12'), (13, b'13'), (14, b'14'), (15, b'15'), (16, b'16'), (17, b'17'), (18, b'18'), (19, b'19'), (20, b'20'), (21, b'21'), (22, b'22'), (23, b'23'), (24, b'24'), (25, b'25'), (26, b'26'), (27, b'27'), (28, b'28'), (29, b'29'), (30, b'30'), (31, b'31'), (32, b'32'), (33, b'33'), (34, b'34'), (35, b'35'), (36, b'36'), (37, b'37'), (38, b'38'), (39, b'39'), (40, b'40'), (41, b'41'), (42, b'42'), (43, b'43'), (44, b'44'), (45, b'45'), (46, b'46'), (47, b'47'), (48, b'48'), (49, b'49'), (50, b'50'), (51, b'51'), (52, b'52'), (53, b'53'), (54, b'54'), (55, b'55'), (56, b'56'), (57, b'57'), (58, b'58'), (59, b'59')])),
                ('start', models.DateTimeField(verbose_name='Start', editable=False)),
                ('end_yyyy', models.IntegerField(blank=True, null=True, verbose_name='End Year', choices=[(1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024)])),
                ('end_mm', models.SmallIntegerField(blank=True, null=True, verbose_name='End Month', choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')])),
                ('end_dd', models.SmallIntegerField(blank=True, null=True, verbose_name='End Day', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31)])),
                ('end_hh', models.SmallIntegerField(blank=True, null=True, verbose_name='End Hour', choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23)])),
                ('end_ii', models.SmallIntegerField(blank=True, null=True, verbose_name='End Minute', choices=[(0, b'00'), (1, b'01'), (2, b'02'), (3, b'03'), (4, b'04'), (5, b'05'), (6, b'06'), (7, b'07'), (8, b'08'), (9, b'09'), (10, b'10'), (11, b'11'), (12, b'12'), (13, b'13'), (14, b'14'), (15, b'15'), (16, b'16'), (17, b'17'), (18, b'18'), (19, b'19'), (20, b'20'), (21, b'21'), (22, b'22'), (23, b'23'), (24, b'24'), (25, b'25'), (26, b'26'), (27, b'27'), (28, b'28'), (29, b'29'), (30, b'30'), (31, b'31'), (32, b'32'), (33, b'33'), (34, b'34'), (35, b'35'), (36, b'36'), (37, b'37'), (38, b'38'), (39, b'39'), (40, b'40'), (41, b'41'), (42, b'42'), (43, b'43'), (44, b'44'), (45, b'45'), (46, b'46'), (47, b'47'), (48, b'48'), (49, b'49'), (50, b'50'), (51, b'51'), (52, b'52'), (53, b'53'), (54, b'54'), (55, b'55'), (56, b'56'), (57, b'57'), (58, b'58'), (59, b'59')])),
                ('end', models.DateTimeField(verbose_name='Start', editable=False)),
                ('is_all_day', models.BooleanField(default=False, verbose_name='All Day Event')),
                ('event', models.ForeignKey(verbose_name='Event', to='events.Event')),
            ],
            options={
                'ordering': ('start',),
                'abstract': False,
                'verbose_name': 'event time',
                'verbose_name_plural': 'event times',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventTimeLabel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('title', base_libs.models.fields.MultilingualCharField(verbose_name='title', max_length=200, null=True, editable=False)),
                ('sort_order', models.IntegerField(default=0, verbose_name='Sort Order')),
                ('title_de', models.CharField(max_length=200, verbose_name='title')),
                ('title_en', models.CharField(max_length=200, verbose_name='title', blank=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'verbose_name': 'Event-time Label',
                'verbose_name_plural': 'Event-time Labels',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('sort_order', models.IntegerField(default=0, verbose_name='sort order', editable=False, blank=True)),
                ('title', base_libs.models.fields.MultilingualCharField(verbose_name='title', max_length=255, null=True, editable=False)),
                ('title_de', models.CharField(max_length=255, verbose_name='title')),
                ('title_en', models.CharField(max_length=255, verbose_name='title', blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='child_set', blank=True, to='events.EventType', null=True)),
            ],
            options={
                'ordering': ['tree_id', 'lft'],
                'verbose_name': 'event type',
                'verbose_name_plural': 'event types',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='eventtime',
            name='label',
            field=models.ForeignKey(related_name='label_event_types', verbose_name='Label', blank=True, to='events.EventTimeLabel', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='event_type',
            field=mptt.fields.TreeForeignKey(related_name='type_events', verbose_name='Event type', to='events.EventType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='im0_type',
            field=models.ForeignKey(related_name='events0', verbose_name='IM Type', blank=True, to='optionset.IMType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='im1_type',
            field=models.ForeignKey(related_name='events1', verbose_name='IM Type', blank=True, to='optionset.IMType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='im2_type',
            field=models.ForeignKey(related_name='events2', verbose_name='IM Type', blank=True, to='optionset.IMType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='modifier',
            field=models.ForeignKey(related_name='event_modifier', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modifier'),
            preserve_default=True,
        ),
    ]
