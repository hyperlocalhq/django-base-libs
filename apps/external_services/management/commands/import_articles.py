# -*- coding: UTF-8 -*-
from django.core.management.base import BaseCommand
from django.utils.encoding import force_text

SILENT, NORMAL, VERBOSE = 0, 1, 2


class Command(BaseCommand):
    help = """Imports articles from the article-import sources"""

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity', NORMAL))
        import re
        import requests
        from requests.exceptions import ConnectionError, ReadTimeout
        from xml.dom.minidom import parseString
        from dateutil.parser import parse as parse_datetime

        from django.apps import apps
        from django.db import models
        from django.core.exceptions import MultipleObjectsReturned
        from django.db import IntegrityError

        from base_libs.utils.misc import get_related_queryset
        from base_libs.utils.betterslugify import better_slugify
        from base_libs.models.base_libs_settings import STATUS_CODE_PUBLISHED, MARKUP_HTML_WYSIWYG

        from jetson.apps.external_services.utils import get_value
        from jetson.apps.external_services.utils import date_de_to_en

        Article = apps.get_model("articles", "Article")
        ArticleImportSource = apps.get_model("external_services", "ArticleImportSource")
        ObjectMapper = apps.get_model("external_services", "ObjectMapper")

        default_article_type = get_related_queryset(
            Article,
            "article_type",
        ).get(slug="news")

        services_failed = []
        articles_failed = []

        for s in ArticleImportSource.objects.all():
            self.stdout.write(u"Importing from {}\n".format(s.url))
            try:
                response = requests.get(
                    s.url,
                    allow_redirects=True,
                    verify=False,
                    headers={
                        'User-Agent': 'Creative City Berlin',
                    }
                )
            except (ConnectionError, ReadTimeout):
                services_failed.append(s)
                self.stdout.write(u" - failed\n")
                continue

            if response.status_code != 200:
                services_failed.append(s)
                self.stdout.write(u" - failed\n")
                continue
            data = response.content  # bytestring, not necessarily utf-8

            # quick fix of broken feeds
            data = data.replace("& ", "&amp; ")
            data = re.sub(r'<trackback:ping>[\s\S]*?</trackback:ping>', '', data)  # remove dasauge-specific invalid tags

            try:
                xml_doc = parseString(data)
            except Exception:
                services_failed.append(s)
                continue

            for node_article in xml_doc.getElementsByTagName("item"):
                external_id = (
                    get_value(node_article, "guid")  # if guid is not provided
                    or get_value(node_article, "link")  # use link as external_id
                )
                publishing_date = get_value(node_article, "pubDate")
                if not publishing_date:
                    self.stderr.write(u"No publishing date provided for article with external id {}\n".format(external_id))
                    continue
                change_date = parse_datetime(
                    date_de_to_en(publishing_date),
                    ignoretz=True,
                )

                # get or create article
                mapper = None
                try:
                    # get article from saved mapper
                    mapper = s.objectmapper_set.get(
                        external_id=external_id,
                        content_type__app_label="articles",
                        content_type__model="article",
                    )
                except models.ObjectDoesNotExist:
                    # or create a new article and then create a mapper
                    article = Article()
                except MultipleObjectsReturned:
                    self.stderr.write(u"Database integrity error with article which external_id is {}.\n".format(external_id))
                    continue
                else:
                    article = mapper.content_object
                    if not article:
                        # if article was deleted after import,
                        # don't import it again
                        continue
                    if article.modified_date:
                        if article.modified_date > change_date or article.status == STATUS_CODE_PUBLISHED:
                            continue

                article.orig_published = change_date
                article.published_from = change_date

                article.title = get_value(node_article, "title")
                article.slug = better_slugify(article.title)

                content = get_value(node_article, "content:encoded") or get_value(node_article, "description")
                if "</p>" not in content:
                    content = "<p>%s</p>" % content
                article.content = content
                article.content_markup_type = MARKUP_HTML_WYSIWYG

                article.language = article.guess_language()

                article.external_url = get_value(node_article, "link")
                # set whether it's an excerpt
                article.is_excerpt = s.are_excerpts

                # set article type
                article.article_type = default_article_type

                # set status
                article.status = s.default_status

                # set content provider
                article.content_provider = s.content_provider

                try:
                    article.save()
                except Exception:
                    articles_failed.append(article)
                    continue

                self.stdout.write(u" - {} (id={}, external_id={})\n".format(article.title, article.pk, external_id))

                # set sites
                article.sites.clear()
                for site in s.default_sites.all():
                    try:
                        article.sites.add(site)
                    except IntegrityError:  # let's ignore the mysterious database integrity error
                        pass

                # set creative sectors
                article.creative_sectors.clear()
                for cs in s.default_creative_sectors.all():
                    try:
                        article.creative_sectors.add(cs)
                    except IntegrityError:  # let's ignore the mysterious database integrity error
                        pass

                # set categories
                article.categories.clear()
                for cat in s.default_categories.all():
                    try:
                        article.categories.add(cat)
                    except IntegrityError:  # let's ignore the mysterious database integrity error
                        pass

                if not mapper:
                    mapper = ObjectMapper(
                        service=s,
                        external_id=external_id,
                    )
                    mapper.content_object = article
                    mapper.save()

        if verbosity > NORMAL:
            self.stdout.write(u"Services failed: {}\n".format(len(services_failed)))
            for s in services_failed:
                self.stdout.write(u"    {}\n".format(s.url))
            self.stdout.write(u"Articles failed: {}\n".format(len(articles_failed)))
            for a in articles_failed:
                self.stdout.write(u"    {}\n".format(a.external_url))
