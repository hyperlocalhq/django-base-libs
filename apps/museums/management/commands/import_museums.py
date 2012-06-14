# -*- coding: UTF-8 -*-
from django.core.management.base import BaseCommand
from django.db import models
from django.conf import settings
from django.core.management import call_command
from optparse import make_option

SILENT, NORMAL, VERBOSE = 0, 1, 2

class Command(BaseCommand):
    help = "imports museums"
    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity', NORMAL))
        import os
        import xlrd
        from base_libs.utils.misc import get_related_queryset
        from django.core.files import File
        
        image_mods = models.get_app("image_mods")

        MuseumCategory = models.get_model("museums", "MuseumCategory")
        Museum = models.get_model("museums", "Museum")
        
        mc_architecture = MuseumCategory.objects.get(slug="arch-kg-design")
        mc_archeology = MuseumCategory.objects.get(slug="archaologie")
        mc_aussereurope = MuseumCategory.objects.get(slug="aussereurop-kult")
        mc_berlinergeschichte = MuseumCategory.objects.get(slug="berlingeschichte")
        mc_photography = MuseumCategory.objects.get(slug="fotogr-film-fern")
        mc_gedenkstaetten = MuseumCategory.objects.get(slug="gedenkstatten")
        mc_gegenwartskunst = MuseumCategory.objects.get(slug="gegenwartskunst")
        mc_kultgeschichte = MuseumCategory.objects.get(slug="kult")
        mc_kunstbis1900 = MuseumCategory.objects.get(slug="kunst-bis-1900")
        mc_kunstdes20jhd = MuseumCategory.objects.get(slug="kunst-des-20-jhd")
        mc_technik = MuseumCategory.objects.get(slug="naturwisstechnik")
        mc_gaerten = MuseumCategory.objects.get(slug="schlossergarten")
        mc_theater = MuseumCategory.objects.get(slug="theater-lit-mus")
        mc_zeitgeschichte = MuseumCategory.objects.get(slug="zeitgeschichte")
        mc_kinder = MuseumCategory.objects.get(slug="kinder-jug")

        wb = xlrd.open_workbook('import/museums.xls')
        
        # import artistic institutions
        sh = wb.sheet_by_index(0)
        for rownum in range(sh.nrows):
            if rownum >= 2: # skip the first two rows
                (
                    title,
                    street_address,
                    postal_code,
                    city,
                    phone,
                    phone2,
                    fax,
                    additional_street_address,
                    email,
                    website,
                    image_caption,
                    cat_architecture,
                    cat_archeology,
                    cat_aussereurope,
                    cat_berlinergeschichte,
                    cat_photography,
                    cat_gedenkstaetten,
                    cat_gegenwartskunst,
                    cat_kultgeschichte,
                    cat_kunstbis1900,
                    cat_kunstdes20jhd,
                    cat_technik,
                    cat_gaerten,
                    cat_theater,
                    cat_zeitgeschichte,
                    cat_kinder,
                    ) = sh.row_values(rownum)
                    
                museum = Museum()
                museum.title_de = museum.title_en = title
                museum.street_address = street_address
                museum.postal_code = str(postal_code).replace(".0", "")
                museum.city = city
                museum.phone = phone
                museum.fax = fax
                museum.email = email.replace("(at)", "@")
                museum.website = website
                museum.image_caption_de = museum.image_caption_en = image_caption
                museum.image_caption_de_markup_type = museum.image_caption_en_markup_type = "pt"
                museum.status = "published"
                museum.save()
                
                try:
                    f = File(open(os.path.join(settings.ROOT_PATH, "museumsportal", "import", "museums_img", "%d.jpg" % (rownum + 1)), "r"))
                except IOError:
                    pass
                else:
                    image_mods.FileManager.save_file_for_object(
                        museum,
                        "%s.jpg" % museum.slug,
                        f,
                        subpath = "museums/",
                        use_timestamp=False,
                        )
                
                if cat_architecture:
                    museum.categories.add(mc_architecture)
                if cat_archeology:
                    museum.categories.add(mc_archeology)
                if cat_aussereurope:
                    museum.categories.add(mc_aussereurope)
                if cat_berlinergeschichte:
                    museum.categories.add(mc_berlinergeschichte)
                if cat_photography:
                    museum.categories.add(mc_photography)
                if cat_gedenkstaetten:
                    museum.categories.add(mc_gedenkstaetten)
                if cat_gegenwartskunst:
                    museum.categories.add(mc_gegenwartskunst)
                if cat_kultgeschichte:
                    museum.categories.add(mc_kultgeschichte)
                if cat_kunstbis1900:
                    museum.categories.add(mc_kunstbis1900)
                if cat_kunstdes20jhd:
                    museum.categories.add(mc_kunstdes20jhd)
                if cat_technik:
                    museum.categories.add(mc_technik)
                if cat_gaerten:
                    museum.categories.add(mc_gaerten)
                if cat_theater:
                    museum.categories.add(mc_theater)
                if cat_zeitgeschichte:
                    museum.categories.add(mc_zeitgeschichte)
                if cat_kinder:
                    museum.categories.add(mc_kinder)
                
                if verbosity == 2:
                    print "%s imported" % museum.title
                    print "Categories: %s" % museum.categories.all()

