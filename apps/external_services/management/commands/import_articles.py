# -*- coding: UTF-8 -*-
from django.core.management.base import NoArgsCommand

SILENT, NORMAL, VERBOSE = 0, 1, 2


class Command(NoArgsCommand):
    help = """Imports articles from the article-import sources"""

    def handle_noargs(self, **options):
        verbosity = int(options.get('verbosity', NORMAL))

        from xml.dom.minidom import parseString
        from dateutil.parser import parse as parse_datetime
        from urllib2 import URLError

        from django.db import models
        from django.core.exceptions import MultipleObjectsReturned
        from django.template.defaultfilters import slugify

        from base_libs.utils.misc import get_related_queryset
        from base_libs.models.base_libs_settings import STATUS_CODE_PUBLISHED, MARKUP_HTML_WYSIWYG
        from base_libs.utils.client import Connection

        from jetson.apps.external_services.utils import get_value
        from jetson.apps.external_services.utils import date_de_to_en

        Article = models.get_model("articles", "Article")
        ArticleImportSource = models.get_model("external_services", "ArticleImportSource")
        ObjectMapper = models.get_model("external_services", "ObjectMapper")

        default_article_type = get_related_queryset(
            Article,
            "article_type",
        ).get(slug="news")

        services_failed = []
        articles_failed = []

        for s in ArticleImportSource.objects.all():
            c = Connection(s.url)
            try:
                r = c.send_request()
            except URLError:
                services_failed.append(s)
                continue
            data = r.read()

            # quick fix of broken feeds
            data = data.replace("& ", "&amp; ")

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
                change_date = parse_datetime(
                    date_de_to_en(get_value(node_article, "pubDate")),
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
                    print u"Database integrity error with article which external_id is %s." % external_id
                    continue
                else:
                    article = mapper.content_object
                    if not article:
                        # if article was deleted after import,
                        # don't import it again
                        continue
                    if article.modified_date > change_date or article.status == STATUS_CODE_PUBLISHED:
                        continue

                article.orig_published = change_date
                article.published_from = change_date

                article.title = get_value(node_article, "title")

                article.slug = slugify(article.title)

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

                # set sites
                article.sites.clear()
                for site in s.default_sites.all():
                    article.sites.add(site)

                # set creative sectors
                article.creative_sectors.clear()
                for cs in s.default_creative_sectors.all():
                    article.creative_sectors.add(cs)

                if verbosity > NORMAL:
                    print article.__dict__

                if not mapper:
                    mapper = ObjectMapper(
                        service=s,
                        external_id=external_id,
                    )
                    mapper.content_object = article
                    mapper.save()

                    if verbosity > NORMAL:
                        print mapper.__dict__
        if verbosity > NORMAL:
            print "Services failed: %d" % len(services_failed)
            for s in services_failed:
                print "    %s" % s.url
            print "Articles failed: %d" % len(articles_failed)
            for a in articles_failed:
                print "    %s" % a.external_url
