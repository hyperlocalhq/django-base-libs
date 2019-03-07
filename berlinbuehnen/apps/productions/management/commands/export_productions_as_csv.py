# -*- coding: UTF-8 -*-
from optparse import make_option

from django.utils.encoding import smart_str
from django.core.management.base import NoArgsCommand
from django.apps import apps

SILENT, NORMAL, VERBOSE, VERY_VERBOSE = 0, 1, 2, 3


class Command(NoArgsCommand):
    help = "Exports productions to productions.csv for machine learning"

    def handle_noargs(self, *args, **options):
        self.verbosity = int(options.get("verbosity", NORMAL))
        self.main()

    def main(self):
        import csv
        from berlinbuehnen.apps.productions.models import Production, ProductionCategory, LanguageAndSubtitles
        categories = list(ProductionCategory.objects.filter(parent=None).order_by('title_de'))
        language_and_subtitles = list(LanguageAndSubtitles.objects.order_by('title_de'))

        with open('productions.csv', 'wb') as csvfile:
            writer = csv.writer(csvfile)
            header = ['id', 'title_de']
            for cat in categories:
                header.append('categories_{}'.format(cat.slug))
            for cat in language_and_subtitles:
                header.append('languages_and_subtitles_{}'.format(cat.slug))
            header += ['free_entrance', 'price_from', 'price_till', 'age_from', 'age_till', 'classiccard']
            writer.writerow(header)

            total = Production.objects.filter(status="published").count()
            for index, prod in enumerate(Production.objects.filter(status="published").order_by("title_de"), 1):
                row = [prod.id, prod.title_de.encode('utf-8')]
                for cat in categories:
                    if prod.categories.filter(tree_id=cat.tree_id):
                        row.append(1)
                    else:
                        row.append(0)
                for cat in language_and_subtitles:
                    if prod.language_and_subtitles == cat:
                        row.append(1)
                    else:
                        row.append(0)
                row.append(1 if prod.free_entrance else 0)
                row.append(float(prod.price_from) if prod.price_from else 0)
                row.append(float(prod.price_till) if prod.price_till else 0)
                row.append(int(prod.age_from) if prod.age_from else 0)
                row.append(int(prod.age_till) if prod.age_till else 0)
                row.append(1 if prod.classiccard else 0)

                writer.writerow(row)
                self.stdout.write(u'{}/{}. {}'.format(index, total, prod.title))
                self.stdout.flush()