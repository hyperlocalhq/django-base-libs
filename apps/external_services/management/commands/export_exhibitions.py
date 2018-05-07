# -*- coding: UTF-8 -*-
# @Author: Daniel Lehmann
# @Date:   2018/04/27
# @Email:  code@dreammedia.info
# @Last modified by:   Daniel Lehmann
# @Last modified time: 2018/05/02
# @copyright Daniel Lehmann (code@dreammedia.info)

from django.core.management.base import BaseCommand, CommandError
from django.db import models, connection
from optparse import make_option

import os
import errno
from shutil import copyfile
from lxml import etree as ET
from django.utils.six.moves import input


from filebrowser.models import FileDescription
Museum = models.get_model("museums", "Museum")
Exhibition = models.get_model("exhibitions", "Exhibition")
Organizer = models.get_model("exhibitions", "Organizer")
Season = models.get_model("exhibitions", "Season")
MediaFile = models.get_model("exhibitions", "MediaFile")
ExhibitionCategory = models.get_model("exhibitions", "ExhibitionCategory")


class Command(BaseCommand):
    help = 'Exports exhibitions to a SQL file. The exported exhibitions can be narrowed down by providing a XML file with museums of the to be exported exhibitions. (see export_museums of LNDM)'

    option_list = BaseCommand.option_list + (
        make_option(
            '--output',
            dest='outputfile',
            metavar="FILE",
            help='the SQL file to write to',
        ),
        make_option(
            '--input',
            dest='inputfile',
            metavar="FILE",
            help='an XML file of museums (see export_museums of LNDM)',
        ),
        make_option(
            '--media',
            dest='mediafolder',
            metavar="FOLDER",
            help='path to a folder where the media files will be copied',
        ),
    )


    def handle(self, *args, **options):

        museums = []

        def _addslashes(s):
            # adds slashes to a string for certain characters
            l = ["\\", '"', "'", "\0", ]
            for i in l:
                if i in s:
                    s = s.replace(i, '\\'+i)
            return s

        def _object_to_query(obj, table, with_id=True):
            # returns an sql insert statment of the "obj" for the "table"
            # dosen't work for many to many tables

            values = [(f, f.get_db_prep_save(f.value_from_object(obj), connection)) for f in obj._meta.local_fields]

            first = True
            text = 'INSERT INTO '+table+' SET '
            for a,b in values:

                # adjusting the field name
                field = str(a.name)
                if field == "museum":
                    field = "museum_id"
                elif field == "exhibition":
                    field = "exhibition_id"
                elif field == "organizing_museum":
                    field = "organizing_museum_id"
                elif field == "parent":
                    field = "parent_id"

                # adjusting the value
                if isinstance(b, (int, long)):
                    if isinstance(b, bool):
                        if b:
                            value = "1"
                        else:
                            value = "0"
                    else:
                        value = str(b)
                else:
                    value = "%s" % b
                    if value == "None":
                        value = "NULL"
                    else:
                        value = "'"+_addslashes(value.encode('utf-8'))+"'"

                # replacing museums ids with the ids of the imported museums
                if field == "museum_id" or field == "organizing_museum_id":
                    for museum_id, import_id in museums:
                        if museum_id == b:
                            value = import_id

                if with_id or field != "id":
                    if not first:
                        text += ", "
                    else:
                        first = False
                    text += field+" = "+value

            text += ";\n"
            return text

        global missing_files
        global file_counter
        missing_files = []
        file_counter = 0
        def _copy(file_browser_field):
            # copies a file from a file_browser_field to the path given in the media argument
            # none existing folders are getting created
            # checks if the media argument is given and if the file_browser_field is not empty
            # returns the file browser SQL code connected to the file_browser_field

            global missing_files
            global file_counter

            sql_code = ''

            if options['mediafolder'] and file_browser_field:

                file = str(file_browser_field)
                #print('copying file '+file)
                file_counter += 1
                if file_counter == 1:
                    print '_',
                if file_counter == 2:
                    print '/',
                if file_counter == 3 or file_counter == 4 or file_counter == 6 or file_counter == 7:
                    print '"',
                if file_counter == 5:
                    print '=',
                if file_counter == 8:
                    print '\\',
                if file_counter == 9:
                    print '_',
                    file_counter = 0

                src = "media/"+file
                dest = options['mediafolder']+"/"+file

                try:
                    os.makedirs(os.path.dirname(dest))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise

                if os.path.isfile(src):
                    copyfile(src, dest)

                    file_descriptions = FileDescription.objects.filter(file_path=file_browser_field)
                    if file_descriptions:
                        sql_code += 'DELETE FROM filebrowser_filedescription WHERE file_path = "'+file+'"'+";\n"
                        for file_description in file_descriptions:
                            sql_code += _object_to_query(file_description, 'filebrowser_filedescription', False)
                else:
                    missing_files.append(file)

            return sql_code


        if (options['inputfile']):
            # trying to match the imported museums to museums in the database

            tree = ET.parse(options['inputfile'])
            root = tree.getroot()

            for entry in root[0]:
                entry_pk = entry.get("pk")
                title_de = entry[0].text
                title_en = entry[1].text

                saved = False
                try:
                    museum = Museum.objects.get(pk=entry_pk)
                except Museum.DoesNotExist:
                    museum = None

                if museum:
                    if museum.title_de == title_de:
                        museums.append((museum.pk, entry_pk))
                        saved = True
                        try:
                            print("Found %s" % museum.title_de)
                        except UnicodeEncodeError as e:
                            print("Found %s" % museum.title_de.encode('utf-8'))
                    else:
                        print('')
                        try:
                            print("Primary key and title_de doesn't match for %s" % title_de)
                            print("Title I found is %s" % museum.title_de)
                        except UnicodeEncodeError as e:
                            print("Primary key and title_de doesn't match for %s" % title_de.encode('utf-8'))
                            print("Title I found is %s" % museum.title_de.encode('utf-8'))

                        result = input("Is this the right museum y/n: ")
                        while len(result) < 1 or result[0].lower() not in "yn":
                            result = input("Please answer y(es) or n(o): ")

                        if result[0].lower() == "y":
                            museums.append((museum.pk, entry_pk))
                            saved = True

                if not saved:
                    museums_query = Museum.objects.filter(title_de__icontains=title_de)
                    print('')
                    try:
                        print("Searched for title_de %s" % title_de)
                    except UnicodeEncodeError as e:
                        print("Searched for title_de %s" % title_de.encode('utf-8'))
                    for museum in museums_query:
                        if museum and not saved:
                            try:
                                print("Found %s" % museum.title_de)
                            except UnicodeEncodeError as e:
                                print("Found %s" % museum.title_de.encode('utf-8'))

                            result = input("Is this the right museum y/n: ")
                            while len(result) < 1 or result[0].lower() not in "yn":
                                result = input("Please answer y(es) or n(o): ")

                            if result[0].lower() == "y":
                                museums.append((museum.pk, entry_pk))
                                saved = True
                    if not saved:
                        print("Couldn't find any museum matching the title_de.")

                if not saved:
                    result = input("Do you want to enter an alternative title_de y/n: ")
                    while len(result) < 1 or result[0].lower() not in "yn":
                        result = input("Please answer y(es) or n(o): ")

                    while result[0].lower() == "y":
                        result = input("Please enter title_de: ")
                        museums_query = Museum.objects.filter(title_de__icontains=result)
                        print('')
                        try:
                            print("Searched for title_de %s" % result)
                        except UnicodeEncodeError as e:
                            print("Searched for title_de %s" % result.encode('utf-8'))

                        for museum in museums_query:
                            if museum and not saved:
                                try:
                                    print("Found %s" % museum.title_de)
                                except UnicodeEncodeError as e:
                                    print("Found %s" % museum.title_de.encode('utf-8'))

                                result = input("Is this the right museum y/n: ")
                                while len(result) < 1 or result[0].lower() not in "yn":
                                    result = input("Please answer y(es) or n(o): ")

                                if result[0].lower() == "y":
                                    museums.append((museum.pk, entry_pk))
                                    saved = True
                                    result = "n"

                        if not saved:
                            print("Couldn't find any museum matching your title_de.")
                            result = input("Do you want to enter another alternative title_de y/n: ")
                            while len(result) < 1 or result[0].lower() not in "yn":
                                result = input("Please answer y(es) or n(o): ")



                if not saved:
                    print('')
                    try:
                        print("Couldn't match to entry for %s" % title_de)
                    except UnicodeEncodeError as e:
                        print("Couldn't match to entry for %s" % title_de.encode('utf-8'))
                    print('')


        # getting the exhibitions
        if len(museums) == 0:
            exhibitions = Exhibition.objects.all()
        else:
            museums_pk = []
            for pk, dummy in museums:
                museums_pk.append(pk)
            exhibitions = Exhibition.objects.filter(museum__pk__in=museums_pk)


        # creating the SQL statments
        print('')
        if options['mediafolder']:
            print 'Copying files to folder '+options['mediafolder']+' ...',

        sql_exhibitioncategory = "DELETE FROM exhibitions_exhibitioncategory;\n"
        exhibitioncategories = ExhibitionCategory.objects.all()
        for exhibitioncategory in exhibitioncategories:
            sql_exhibitioncategory += _object_to_query(exhibitioncategory, 'exhibitions_exhibitioncategory')

        sql_exhibition = "DELETE FROM exhibitions_exhibition;\n"
        sql_exhibition_categories = "DELETE FROM exhibitions_exhibition_categories;\n"
        sql_mediafile = "DELETE FROM exhibitions_mediafile;\n"
        sql_organizer = "DELETE FROM exhibitions_organizer;\n"
        sql_season = "DELETE FROM exhibitions_season;\n"
        sql_filebrowser = ""
        for exhibition in exhibitions:

            if exhibition.status == "published":

                sql_exhibition += _object_to_query(exhibition, 'exhibitions_exhibition')
                sql_filebrowser += _copy(exhibition.image)
                sql_filebrowser += _copy(exhibition.pdf_document_de)
                sql_filebrowser += _copy(exhibition.pdf_document_en)

                categories = exhibition.categories.all()
                for category in categories:
                    sql_exhibition_categories += 'INSERT INTO exhibitions_exhibition_categories SET exhibition_id = '+str(exhibition.pk)+', exhibitioncategory_id = '+str(category.pk)+";\n"

                mediafiles = MediaFile.objects.filter(exhibition__pk = exhibition.pk)
                for mediafile in mediafiles:
                    sql_mediafile += _object_to_query(mediafile, 'exhibitions_mediafile')
                    sql_filebrowser += _copy(mediafile.path)


                organizers = Organizer.objects.filter(exhibition__pk = exhibition.pk)
                for organizer in organizers:
                    sql_organizer += _object_to_query(organizer, 'exhibitions_organizer')

                seasons = Season.objects.filter(exhibition__pk = exhibition.pk)
                for season in seasons:
                    sql_season += _object_to_query(season, 'exhibitions_season')

        sql_statements = sql_exhibitioncategory+"\n"+sql_exhibition+"\n"+sql_exhibition_categories+"\n"+sql_mediafile+"\n"+sql_organizer+"\n"+sql_season+"\n"+sql_filebrowser

        print('')
        if len(missing_files):
            print('The following files are missing:')
            for missing_file in missing_files:
                print(missing_file)

        # writing the file
        if options['outputfile']:

            try:
                os.makedirs(os.path.dirname(options['outputfile']))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

            with open(options['outputfile'], "w") as text_file:
                text_file.write(sql_statements)

            print('')
            print('Written SQL statments to %s' % options['outputfile'] )

        else:

            print('')
            print('Created Successfully the SQL statments. To write the statments to a file use the argument --output')
