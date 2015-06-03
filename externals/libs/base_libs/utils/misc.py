# -*- coding: UTF-8 -*-
import hashlib
import re
import sys
from datetime import datetime, time
from time import strptime

from django.utils import simplejson
from django.contrib.sites.models import Site
from django.utils.encoding import smart_str, force_unicode
from django.utils.translation import ugettext, get_language, activate
from django.db.models.loading import get_app
from django.db import models
from django.conf import settings
from django.http import Http404


def get_or_404(model, **fields):
    """
    tries to perform a <<model>>.objects.get(<<some_fields_specifiers>>)
    operation to get a specific dataset from a queryset. This is just
    used to minimze code.
    """
    try:
        return model.objects.get(**fields)
    except model.DoesNotExist:
        msg = ""
        for (key, value) in fields.items():
            msg = msg + "%s '%s', " % (key, value)
        msg = msg.strip(", ") 
        raise Http404, "%s with %s cannot be found" %\
         (force_unicode(model._meta.verbose_name), msg)

def get_website_url(path="/"):
    protocol = getattr(settings, "PROTOCOL", "http")
    domain = Site.objects.get_current().domain
    port = getattr(settings, "PORT", "")
    if port:
        assert port.startswith(":"), "The PORT setting must have a preceeding ':'."
    return u"%s://%s%s%s" % (protocol, domain, port, path)

def get_website_ssl_url(path="/"):
    protocol = getattr(settings, "HTTPS_PROTOCOL", "https")
    domain = Site.objects.get_current().domain
    port = getattr(settings, "PORT", "")
    if port:
        assert port.startswith(":"), "The PORT setting must have a preceeding ':'."
    return u"%s://%s%s%s" % (protocol, domain, port, path)

def verify_objref_hash(content_type_id, object_id, hash):
    hash_match = hashlib.sha1("%s/%s" % (content_type_id, object_id) + settings.SECRET_KEY).hexdigest()
    return hash == hash_match

def get_unique_value(model, proposal, field_name="slug", instance_pk=None, separator="-", number_first=False, numbering_from=1, min_width=0, postfix="", postfix_regex="", ignore_case=False):
    """ Returns unique string by the proposed one.
    Format: <proposal>[<separator><number>[<postfix>]]
    By default, for proposal 'example' returns strings from the sequence:
        'example', 'example-2', 'example-3', 'example-4', ...
    Depending on the incoming arguments the results might be from the sequence:
        'example_0000_d0702', 'example_0001_d0704', 'example_0002_d0704', ...
    A queryset can be passed instead of model to the model argument.
    Optionally takes:
    * field name which can  be 'slug', 'username', 'invoice_number', etc.
    * the primary key of the instance to which the string will be assigned.
    * separator which can be '-', '_', ' ', '', etc.
    * number_first: True, when the first value has to be numbered
    * starting number for numbering
    * minimal width of the number to lead by zeros
    * postfix of the value
    * postfix regular expression when may vary
    * ignore_case defines if "Test" should be treated the same as "test"
    """
    qs = getattr(model, "_default_manager", model)
    if not proposal:
        return proposal
    separator_regex = re.escape(separator)
    if postfix and not postfix_regex:
        postfix_regex = re.escape(postfix)
    if ignore_case:
        similar_ones = qs.filter(**{field_name + "__istartswith": proposal})
    else:
        similar_ones = qs.filter(**{field_name + "__startswith": proposal})
    if instance_pk:
        similar_ones = similar_ones.exclude(pk=instance_pk)
    similar_ones = similar_ones.values(field_name)
    if ignore_case:
        similar_ones = [elem[field_name].lower() for elem in similar_ones]
    else:
        similar_ones = [elem[field_name] for elem in similar_ones]
    
    first_result = number_first and "%s%s%0*d%s" % (proposal, separator, min_width, numbering_from, postfix) or proposal
    if ignore_case:
        first_result = first_result.lower()
        
    if first_result not in similar_ones:
        return first_result
    else:
        numbers = []
        for value in similar_ones:
            match = re.match(r'^%s%s(\d+)%s$' % (proposal, separator_regex, postfix_regex), value)
            if match:
                numbers.append(int(match.group(1)))
        number = 1 + (len(numbers) and sorted(numbers)[-1] or numbering_from)
        return "%s%s%0*d%s" % (proposal, separator, min_width, number, postfix)

def get_translation(message, language=None):
    current_lang = get_language()
    activate(language or "en")
    message = ugettext(message)
    activate(current_lang)
    return message

"""
class Currency(float):
    def __init__(self, amount):
        self.amount = amount
    def __str__(self):
        temp = "%.2f" % self.amount
        profile = re.compile(r"(\d)(\d\d\d[,.])")
        while 1:
            temp, count = re.subn(profile,r"\1,\2",temp)
            print temp
            if not count: break
            return temp

    def __unicode__(self):
        temp = "%.2f" % self.amount
        profile = re.compile(r"(\d)(\d\d\d[,.])")
        while 1:
            temp, count = re.subn(profile,r"\1,\2",temp)
            print temp
            if not count: break
            return temp

"""

def html_to_plain_text(html):
    text = smart_str(html)
    def to_utf8(match_obj):
        return unichr(long(match_obj.group(1)))
    coded_entity_pattern = re.compile(r'&#[^;];')
    whitespace_pattern = re.compile(r'\s+')
    line_break_pattern = re.compile(r'<br[^>]+>\s*', re.I)
    new_line_pattern = re.compile(r'<\/(?:p|h1|h2|h3|h4|h5|h6|ul|ol|li|dl)>\s*', re.I)
    link_pattern = re.compile(
        r'<a [^>]*?href=(["\'])([^\1]+?)\1[^>]*?>(.+?)</a>',
        re.I,
        )
    removables_pattern = re.compile(
        r'<(style|script) ?[^>]*>(.+?)</\1>',
        re.I,
        )
    html_tag_pattern = re.compile(r'<[^>]+>')
    html_entity_pattern = re.compile(r'&[^;]+;')
    html_entities = {"&quot;": '"', "&apos;": "'", "&amp;": "&", "&lt;": "<", "&gt;": ">", "&nbsp;": " ", "&iexcl;": "¡", "&curren;": "¤", "&cent;": "¢", "&pound;": "£", "&yen;": "¥", "&brvbar;": "¦", "&sect;": "§", "&uml;": "¨", "&copy;": "©", "&ordf;": "ª", "&laquo;": "«", "&not;": "¬", "&shy;": "­", "&reg;": "®", "&trade;": "™", "&macr;": "¯", "&deg;": "°", "&plusmn;": "±", "&sup2;": "²", "&sup3;": "³", "&acute;": "´", "&micro;": "µ", "&para;": "¶", "&middot;": "·", "&cedil;": "¸", "&sup1;": "¹", "&ordm;": "º", "&raquo;": "»", "&frac14;": "¼", "&frac12;": "½", "&frac34;": "¾", "&iquest;": "¿", "&times;": "×", "&divide;": "÷", "&Agrave;": "À", "&Aacute;": "Á", "&Acirc;": "Â", "&Atilde;": "Ã", "&Auml;": "Ä", "&Aring;": "Å", "&AElig;": "Æ", "&Ccedil;": "Ç", "&Egrave;": "È", "&Eacute;": "É", "&Ecirc;": "Ê", "&Euml;": "Ë", "&Igrave;": "Ì", "&Iacute;": "Í", "&Icirc;": "Î", "&Iuml;": "Ï", "&ETH;": "Ð", "&Ntilde;": "Ñ", "&Ograve;": "Ò", "&Oacute;": "Ó", "&Ocirc;": "Ô", "&Otilde;": "Õ", "&Ouml;": "Ö", "&Oslash;": "Ø", "&Ugrave;": "Ù", "&Uacute;": "Ú", "&Ucirc;": "Û", "&Uuml;": "Ü", "&Yacute;": "Ý", "&THORN;": "Þ", "&szlig;": "ß", "&agrave;": "à", "&aacute;": "á", "&acirc;": "â", "&atilde;": "ã", "&auml;": "ä", "&aring;": "å", "&aelig;": "æ", "&ccedil;": "ç", "&egrave;": "è", "&eacute;": "é", "&ecirc;": "ê", "&euml;": "ë", "&igrave;": "ì", "&iacute;": "í", "&icirc;": "î", "&iuml;": "ï", "&eth;": "ð", "&ntilde;": "ñ", "&ograve;": "ò", "&oacute;": "ó", "&ocirc;": "ô", "&otilde;": "õ", "&ouml;": "ö", "&oslash;": "ø", "&ugrave;": "ù", "&uacute;": "ú", "&ucirc;": "û", "&uuml;": "ü", "&yacute;": "ý", "&thorn;": "þ", "&yuml;": "ÿ", "&OElig;": "Œ", "&oelig;": "œ", "&Scaron;": "Š", "&scaron;": "š", "&Yuml;": "Ÿ", "&circ;": "ˆ", "&tilde;": "˜", "&ensp;": " ", "&emsp;": " ", "&thinsp;": " ", "&zwnj;": " ", "&zwj;": " ", "&lrm;": " ", "&rlm;": " ", "&ndash;": "–", "&mdash;": "—", "&lsquo;": "‘", "&rsquo;": "’", "&sbquo;": "‚", "&ldquo;": "“", "&rdquo;": "”", "&bdquo;": "„", "&dagger;": "†", "&Dagger;": "‡", "&hellip;": "…", "&permil;": "‰", "&lsaquo;": "‹", "&rsaquo;": "›", "&euro;": "€",}
    text = re.sub(removables_pattern, '', text)
    text = re.sub(whitespace_pattern, ' ', text)
    text = re.sub(line_break_pattern, '\n', text)
    text = re.sub(new_line_pattern, '\n\n', text)
    # <a href="URL">NAME</a> -> NAME (URL)
    text = re.sub(link_pattern, r'\3 (\2)', text)
    # remove the rest html tags
    text = re.sub(html_tag_pattern, '', text)
    
    # &<word-based>; -> <special symbol>
    for k, v in html_entities.items():
        text = text.replace(k, v)
    # &#<unicode-number-based>; -> <special symbol>
    text = re.sub(coded_entity_pattern, to_utf8, text)
    # remove the rest html entities
    text = re.sub(html_entity_pattern, '', text)
    return text

def get_related_queryset(model, field_name):
    """
    Get the queryset for the choices of the field in a model
    Example:
        types = get_related_queryset(Person, "individual_type")
    """
    f = model._meta.get_field(field_name)
    qs = f.rel.to._default_manager.complex_filter(f.rel.limit_choices_to)
    return qs

class XChoiceList(list):
    """ List of choices.
    Takes a function, queryset or list as a parameter and returns the list only when iterating,
    """
    def __init__(self, sequence=None, null_choice_text="-"*9):
        self.sequence = sequence
        self.null_choice_text = null_choice_text
    def __iter__(self):
        return iter(self._get_list())
    def __getitem__(self, k):
        return self._get_list()[k]
    def __nonzero__(self):
        return bool(self.sequence)
    def __len__(self):
        return len(self.sequence)
    def __str__(self):
        return str(self._get_list())
    def __unicode__(self):
        return unicode(self._get_list())
    def __repr__(self):
        return repr(self._get_list())
    def _get_list(self):
        if hasattr(self.sequence, "model"):
            result = [("", self.null_choice_text)] + [
                (el.id, hasattr(el, "get_title") and el.get_title() or force_unicode(el))
                for el in self.sequence
                ]
        elif callable(self.sequence):
            result = self.sequence()
            if result:
                result[0] = ("", self.null_choice_text)
            else:
                result = [("", self.null_choice_text)]
        else:
            result = self.sequence
            if result:
                result[0] = ("", self.null_choice_text)
            else:
                result = [("", self.null_choice_text)]
        if self.null_choice_text is None:
            del result[0]
        return result

class ExtendedJSONEncoder(simplejson.JSONEncoder):
    def default(self, o, markers=None):
        if isinstance(o, models.Model):
            return o.__dict__
        if isinstance(o, datetime):
            return {
                'year': o.year,
                'month': o.month,
                'day': o.day,
                'hour': o.hour,
                'minute': o.minute,
                'second': o.second,
                'microsecond': o.microsecond,
            }
        if isinstance(o, time):
            return {
                'hour': o.hour,
                'minute': o.minute,
                'second': o.second,
                'microsecond': o.microsecond,
            }
        if hasattr(o, "path"): # FileObject
            return o.path
        if type(o).__name__ == "ModelState":
            return None
        return simplejson.JSONEncoder.default(self, o)

def get_media_svn_revision(prefix="", postfix=""):
    from django.utils.version import get_svn_revision
    rev = get_svn_revision(settings.MEDIA_ROOT) # "SVN-1234" or "SVN-unknown"
    rev = re.sub(r"[^0-9]+", "", rev) # "1234" or ""
    if rev:
        rev = "".join((prefix, rev, postfix))
    return rev

def get_installed(path):
    """
    Get a module, class, function, or variable from an installed application wherever it is located
    
    Usage:
    
        attr = get_installed("<app_name>{.<module>*}.<attr>")

    Example:
    
        func = get_installed("accounts.views.register")
        mod = get_installed("utils.dynamicforms")
        func = get_installed("auth.create_superuser.createsuperuser")
        
    """
    path_bits = path.split(".")
    app_name = path_bits.pop(0)
    ret_var = path_bits.pop()
    app_path_bits = get_app(app_name).__name__.split(".")[:-1]
    module_path = ".".join(app_path_bits + path_bits)
    m = __import__(module_path, globals(), locals(), '*')
    return getattr(m, ret_var)

def path_in_installed_app(path):
    """
    Get a python path for a module, class, function, or variable
    in the installed application wherever it is located
    
    Usage:
    
        path = path_in_installed_app("<app_name>{.<module>*}.<attr>")

    Example:
    
        path = get_installed("filebrowser.urls")
        # "filebrowser.urls"
        
        path = get_installed("site_specific.misc")
        # "myproject.apps.site_specific.misc"
        
    """
    path_bits = path.split(".")
    app_name = path_bits.pop(0)
    #ret_var = path_bits.pop()
    app_path_bits = get_app(app_name).__name__.split(".")[:-1]
    module_path = ".".join(app_path_bits + path_bits)
    return module_path

def is_installed(path):
    try:
        get_installed(path)
    except:
        return False
    return True

def db_table_exists(model):
    """ Checks if database table for a model exists """
    from django.db import connection, transaction
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT 1 FROM %s LIMIT 1" % model._meta.db_table)
        return True
    except:
        pass
    return False
        

    
    
def truncwords(value, nof_words):
    
    """
    Truncate a string to the specified number of words, similar
    to Django's truncatewords filter but preserves linefeeds
    Argument: Number of words to truncate after.
    """
    
    try:
        length = int(nof_words)
    except ValueError:
        return value
    
    # break into words, retaining linefeeds
    words = []
    for line in value.split('\n'):
        words.extend(line.split(' '))
        words.append('\n')
        length += 1
        if len(words) > length:
            break

    # remove last linefeed
    words.pop()
    length -= 1
    
    if len(words) > length:
        words = words[:length]
        if not words[-1].endswith('...'):
            words.append('...')
    return ' '.join(words).replace(' \n ', '\n')

RFC2822_DATE_FORMAT = "RFC822"

def string_to_datetime(date_string, format):
    """
    utility function: just converts a string given 
    in the specified datetime format to a datetime
    object
    """
    if format == RFC2822_DATE_FORMAT:
        import rfc822
        d = datetime(*rfc822.parsedate(date_string)[:7])
    else:
        if sys.version_info[1] == 5:
            d = strptime(date_string, format)
        else:
            # the python 2.4 version
            d = datetime(*(strptime(date_string, format)[0:6]))
    return d

def smart_truncate(text, length=100, suffix='...'):
    """
    Truncates `text`, on a word boundary, as close to
    the target length it can come.    
    """    
    slen = len(suffix)
    pattern = r'^(.{0,%d}\S)\s+\S+' % (length-slen-1)
    if len(text) > length:
        match = re.match(pattern, text) 
        if match:
            length0 = match.end(0)
            length1 = match.end(1)
            if abs(length0+slen-length) < abs(length1+slen-length): 
                return match.group(0) + suffix
            else:
                return match.group(1) + suffix    
    return text

def get_unused_languages():
    from django.conf import global_settings
    installed_languages = [
        lang[0]
        for lang in settings.LANGUAGES
        ]
    available_languages = [
        lang[0]
        for lang in global_settings.LANGUAGES
        if len(lang[0])==2
        ]
    unused_languages = [
        lang
        for lang in available_languages
        if lang not in installed_languages
        ]
    return unused_languages
    
def south_clean_multilingual_fields(models_dict):
    """
    takes a dictionary of models and fields and
    removes unused localized fields
    """
    unused_languages = get_unused_languages()
    
    
    # Let's consider that field names ending with "_" + any unused language code
    # are parts of unused multilingual which have to be deleted.
    # In addition, their companions with _markup_type will be deleted.
    
    delete_pattern = re.compile(r'_(%s)(_markup_type)?$' % "|".join(unused_languages))
    to_delete = []

    for m in models_dict:
        for f in models_dict[m]:
            if delete_pattern.search(f):
                to_delete.append((m, f))
    
    for m, f in to_delete:
        del models_dict[m][f]
                
    '''                
    multilingual_fields = []
    for m in models_dict:
        for f in models_dict[m]:
            if f not in ("Meta", "_stub"):
                if "Multilingual" in models_dict[m][f][0]:
                    multilingual_fields.append((m, f))
                
    for m, f in multilingual_fields:
        for lang in unused_languages:
            localized_field = "%s_%s" % (f, lang)
            if localized_field in models_dict[m]:
                del models_dict[m][localized_field]
            localized_field_mt = "%s_%s_markup_type" % (f, lang)
            if localized_field_mt in models_dict[m]:
                del models_dict[m][localized_field_mt]
    '''            
    # nothing is returned, because the incoming dictionary is modified directly
    
def south_cleaned_fields(field_list):
    """
    takes an iterable of 2-tuples with field name and field object
    and returns a list of 2-tuples without unused localized fields
    """
    unused_languages = get_unused_languages()
    
    # collect fields that have translatable fields
    multilingual_fields = []
    for fieldname, field in field_list:
        if type(field).__name__.startswith("Multilingual"):
            multilingual_fields.append(fieldname)

    # collect field names that shouldn't be listed
    field_names = dict(field_list).keys()
    fields_to_skip = []
    for f in multilingual_fields:
        for lang in unused_languages:
            localized_field = "%s_%s" % (f, lang)
            if localized_field in field_names:
                fields_to_skip.append(localized_field)
            localized_field_mt = "%s_%s_markup_type" % (f, lang)
            if localized_field_mt in field_names:
                fields_to_skip.append(localized_field_mt)

    # recreate the list of fields
    new_field_list = []
    for fieldname, field in field_list:
        if fieldname not in fields_to_skip:
            new_field_list.append((fieldname, field))
            
    return new_field_list
