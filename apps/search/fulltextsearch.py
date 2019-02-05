# -*- coding: UTF-8 -*-
import re

from django.db.models.query import Q
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode
from django.utils.html import escape
from django.conf import settings

from base_libs.models.query import ExtendedQuerySet


# stemming stuff
from ccb.apps.search.stemming_english import PorterStemmerEnglish
from ccb.apps.search.stemming_german import PorterStemmerGerman

german_mapper = {
    u"ä": "&auml;",
    u"ö": "&ouml;",
    u"ü": "&uuml;",
    u"Ä": "&Auml;",
    u"Ö": "&Ouml;",
    u"Ü": "&Uuml;",
    u"ß": "&szlig;",
}


def full_escape(text):
    new_text = escape(text)
    # replace german letters
    for item in german_mapper:
        new_text = new_text.replace(item, german_mapper[item])
    return new_text


class MySqlFulltextSearchQuerySet(ExtendedQuerySet):
    def __init__(self, model=None, query=None, fields=None, *args, **kwargs):
        super(MySqlFulltextSearchQuerySet, self).__init__(model, query, *args, **kwargs)
        self._search_fields = fields
        self.has_relevance_attr = False

    def _clone(self, *args, **kwargs):
        clone = super(MySqlFulltextSearchQuerySet, self)._clone(*args, **kwargs)
        clone._search_fields = self._search_fields
        clone.has_relevance_attr = self.has_relevance_attr
        return clone

    def get_sort_order_mapper(self):
        sort_order_mapper = {
            'alphabetical_asc': (2, _('Alphabetical (A-Z)'), self.model.objects._get_title_fields()),
            'alphabetical_desc': (3, _('Alphabetical (Z-A)'), self.model.objects._get_title_fields('-')),
            'creation_date_asc': (4, _('Creation date (oldest first)'), ['creation_date']),
            'creation_date_desc': (5, _('Creation date (newest first)'), ['-creation_date']),
        }
        if self.has_relevance_attr:
            sort_order_mapper['relevance'] = (1, _('Relevance'), ['-relevance'])
        return sort_order_mapper

    def search(self, query=None):
        query = query or ""
        meta = self.model._meta

        # Get the table name and column names from the model
        # in `table_name`.`column_name` style
        columns = [meta.get_field(name, many_to_many=True).column for name in self._search_fields]

        full_names = ["%s.%s" % (meta.db_table, column) for column in columns]

        # Create the MATCH…AGAINST expressions

        # some chars are replaced by nothing to avoid parse errors.
        query = query.replace("'", "")
        query = query.replace("(", "")
        query = query.replace(")", "")
        query = query.replace("+", "")
        query = query.strip("-")
        query = query.replace("~", "")
        query = query.replace("*", "")
        query = query.replace("<", "")
        query = query.replace(">", "")
        query = query.replace('"', "")
        query = query.replace('%', "")

        # keyword_list = re.findall(r'\".*?\"|\w+', force_unicode(query), re.UNICODE)
        keywords = re.split('\s+', force_unicode(query), re.UNICODE)

        """
        remove all words of length < 4, because Mysql fulltext search will 
        not look for any words with length < 4 with default settings
        
        Rupert 16102008 We should remove the stopword list and the
        default restriction of min_length of keyqwords = 4 in the mysql
        settings (my.ini, my.conf respectively)
        
        The mysql settings should be applied by
        
        [mysqld]
        ft_min_word_len=2
        ft_stopword_file=""

        [myisamchk]
        ft_min_word_len=2
        ft_stopword_file="" 
        """
        keyword_list = []
        for keyword in keywords:
            if len(keyword) > 0:
                keyword_list.append(keyword)

        """
        build a "keyword alternative list" by escaped words (maybe, there is some
        html in the database, so, we also have to search for those
        escaped sequences. Additionally, a wildcarded stemmed version 
        of the word is added.
        """
        alternatives = {}

        for item in keyword_list:
            alternatives[item] = set()

            esc_item = full_escape(item)
            if esc_item != item:
                alternatives[item].add((esc_item, ""))

            # add stemmed words to alternatives!
            stemmed_english = PorterStemmerEnglish().stem(item, 0, len(item) - 1)
            if stemmed_english != item:
                alternatives[item].add((stemmed_english, "*"))

            stemmed_list_german = PorterStemmerGerman().stem(item)
            for stemmed_german in stemmed_list_german:
                if stemmed_german != item:
                    alternatives[item].add((stemmed_german, "*"))
                    esc_stemmed_german = full_escape(stemmed_german)
                    if esc_stemmed_german != stemmed_german:
                        alternatives[item].add((esc_stemmed_german, "*"))

        keywords_where = ""
        keywords_relevance = ""
        for item in keyword_list:
            if alternatives.has_key(item) and len(alternatives[item]) > 0:
                keyword_where_part = '+(%s' % item
                keyword_relevance_part = '(%s' % item

                for alternative in alternatives[item]:
                    keyword_where_part += ' %s%s' % (alternative[0], alternative[1])
                    keyword_relevance_part += ' %s%s' % (alternative[0], alternative[1])

                keyword_where_part += ')'
                keyword_relevance_part += ')'
            else:
                keyword_where_part = '+%s' % item
                keyword_relevance_part = '%s' % item

            keywords_where = keywords_where + keyword_where_part + " "
            keywords_relevance = keywords_relevance + keyword_relevance_part + " "

        keywords_where = keywords_where.strip(" ")
        keywords_relevance = keywords_relevance.strip(" ")

        fulltext_columns = ", ".join(full_names)
        relevance_expr = "MATCH(%s) AGAINST ('%s')" % (fulltext_columns, keywords_relevance)
        match_expr = "MATCH(%s) AGAINST ('%s' IN BOOLEAN MODE)" % (fulltext_columns, keywords_where)

        if query is None or len(query) == 0:
            # if there is no text for the fulltextsearch, relevance is not available!!!
            self.has_relevance_attr = False
            return self.extra(
                select={'relevance': 1}
            )
        else:
            self.has_relevance_attr = True
            # that stuff is from the real "text colums"
            return self.extra(
                select={'relevance': relevance_expr},
                where=[match_expr + "> 0"]
            )


class ProprietarySearchQuerySet(ExtendedQuerySet):
    def __init__(self, model=None, query=None, fields=None):
        super(ProprietarySearchQuerySet, self).__init__(model, query)
        self._search_fields = fields

    def get_sort_order_mapper(self):
        sort_order_mapper = {
            'alphabetical_asc': (2, _('Alphabetical (A-Z)'), self.model.objects._get_title_fields()),
            'alphabetical_desc': (3, _('Alphabetical (Z-A)'), self.model.objects._get_title_fields('-')),
            'creation_date_asc': (4, _('Creation date (oldest first)'), ['timestamp']),
            'creation_date_desc': (5, _('Creation date (newest first)'), ['-timestamp']),
        }
        return sort_order_mapper

    def search(self, query=None):
        """
        builds up the search query from the keywords provided as a string
        search is always case-insensitive!!!!
        """
        query = query or ""
        meta = self.model._meta
        columns = [meta.get_field(name, many_to_many=False).column for name in self._search_fields]

        keyword_list = query.split()
        the_filter = None
        for keyword in keyword_list:
            inner_filter = None
            for column in columns:
                filter_part = (
                    Q(**{"%s__iexact" % column: keyword}) |
                    Q(**{"%s__istartswith" % column: keyword}) |
                    Q(**{"%s__iendswith" % column: keyword}) |
                    Q(**{"%s__icontains" % column: keyword})
                )
                # must be ORed
                if inner_filter:
                    inner_filter = inner_filter | filter_part
                else:
                    inner_filter = filter_part
            # must be ANDed        
            if the_filter:
                the_filter = the_filter & inner_filter
            else:
                the_filter = inner_filter

        if query is None or len(query) == 0:
            return self
        else:
            return self.filter(the_filter)


class SphinxSearchQuerySet(ExtendedQuerySet):
    def __init__(self, model=None, query=None, fields=None):
        super(SphinxSearchQuerySet, self).__init__(model, query)
        self._search_fields = fields

    def get_sort_order_mapper(self):
        sort_order_mapper = {
            'rank': (1, _('Rank'), ['@rank']),
            'alphabetical_asc': (2, _('Alphabetical (A-Z)'), self.model.objects._get_title_fields()),
            'alphabetical_desc': (3, _('Alphabetical (Z-A)'), self.model.objects._get_title_fields('-')),
            'creation_date_asc': (4, _('Creation date (oldest first)'), ['timestamp']),
            'creation_date_desc': (5, _('Creation date (newest first)'), ['-timestamp']),
        }
        return sort_order_mapper

    def search(self, query=None):
        query = query or ""
        import djangosphinx

        # ' are replaced by nothing to avoid parse errors. Those chars do not have any relevance
        query = query.replace("'", "")
        p = re.compile(r'\".*?\"|\w+')
        query_list = p.findall(query)

        keywords_where = ""

        for item in query_list:
            keywords_where += '%s ' % item
        keywords_where = keywords_where.strip(" ")

        search = djangosphinx.SphinxSearch(index="creativeberlin_sphinx_index")
        sphinx_result = search.query(keywords_where)  # .order_by('@rank')

        results = sphinx_result._get_sphinx_results()
        if not results:
            return self
        else:
            qs = self.model.objects.filter(pk__in=[r['id'] for r in results['matches']])
            return qs


SEARCH_QUERYSET_MODELS = {
    "MySqlFulltext": MySqlFulltextSearchQuerySet,
    "Proprietary": ProprietarySearchQuerySet,
    "Sphinx": SphinxSearchQuerySet,
}

SearchQuerySet = SEARCH_QUERYSET_MODELS[getattr(settings, "SEARCH_ENGINE", "Proprietary")]
