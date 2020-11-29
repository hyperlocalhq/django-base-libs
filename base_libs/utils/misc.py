# -*- coding: UTF-8 -*-
import hashlib
import json
import re
import sys
from datetime import datetime, time
from decimal import Decimal
from time import strptime

from django.apps import apps
from django.conf import settings
from django.db import models
from django.http import Http404
try:
    from django.utils.encoding import force_text, force_bytes
except ImportError:
    from django.utils.encoding import force_unicode as force_text, smart_str as force_bytes

from django.utils.translation import ugettext, get_language, activate

try:
    unichr
except NameError:
    unichr = chr

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
            msg += "%s '%s', " % (key, value)
        msg = msg.strip(", ")
        raise Http404("%s with %s cannot be found" % (
            force_text(model._meta.verbose_name),
            msg,
        ))


def get_website_url(path=""):
    return settings.WEBSITE_URL + path


def verify_objref_hash(content_type_id, object_id, hash):
    hash_match = hashlib.sha1(
        "%s/%s" % (content_type_id, object_id) + settings.SECRET_KEY
    ).hexdigest()
    return hash == hash_match


def get_unique_value(
    model,
    proposal,
    field_name="slug",
    instance_pk=None,
    separator="-",
    number_first=False,
    numbering_from=1,
    min_width=0,
    postfix="",
    postfix_regex="",
    ignore_case=False,
):
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

    first_result = (
        number_first
        and "%s%s%0*d%s" % (proposal, separator, min_width, numbering_from, postfix)
        or proposal
    )
    if ignore_case:
        first_result = first_result.lower()

    if first_result not in similar_ones:
        return first_result
    else:
        numbers = []
        for value in similar_ones:
            match = re.match(
                r"^%s%s(\d+)%s$" % (proposal, separator_regex, postfix_regex), value
            )
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


def html_to_plain_text(html):
    text = force_bytes(html)

    def to_utf8(match_obj):
        return unichr(long(match_obj.group(1)))

    def link_replacement(match):
        link_text = match.group(3)
        link_url = match.group(2)
        if link_url.startswith("mailto:"):
            link_url = link_url.replace("mailto:", "", 1)
        if link_text == link_url:
            return link_text
        return "{link_text} ({link_url})".format(link_text=link_text, link_url=link_url)

    coded_entity_pattern = re.compile(r"&#[^;];")
    whitespace_pattern = re.compile(r"\s+")
    line_break_pattern = re.compile(r"<br[^>]+>\s*", re.I)
    new_line_pattern = re.compile(r"</(?:p|h1|h2|h3|h4|h5|h6|ul|ol|li|dl)>\s*", re.I)
    link_pattern = re.compile(
        r'<a [^>]*?href=(["\'])([^\1]+?)\1[^>]*?>(.+?)</a>', re.I,
    )
    removables_pattern = re.compile(r"<(style|script) ?[^>]*>(.+?)</\1>", re.I,)
    html_tag_pattern = re.compile(r"<[^>]+>")
    html_entity_pattern = re.compile(r"&[^;]+;")
    html_entities = {
        "&quot;": '"',
        "&apos;": "'",
        "&amp;": "&",
        "&lt;": "<",
        "&gt;": ">",
        "&nbsp;": " ",
        "&iexcl;": "¡",
        "&curren;": "¤",
        "&cent;": "¢",
        "&pound;": "£",
        "&yen;": "¥",
        "&brvbar;": "¦",
        "&sect;": "§",
        "&uml;": "¨",
        "&copy;": "©",
        "&ordf;": "ª",
        "&laquo;": "«",
        "&not;": "¬",
        "&shy;": "­",
        "&reg;": "®",
        "&trade;": "™",
        "&macr;": "¯",
        "&deg;": "°",
        "&plusmn;": "±",
        "&sup2;": "²",
        "&sup3;": "³",
        "&acute;": "´",
        "&micro;": "µ",
        "&para;": "¶",
        "&middot;": "·",
        "&cedil;": "¸",
        "&sup1;": "¹",
        "&ordm;": "º",
        "&raquo;": "»",
        "&frac14;": "¼",
        "&frac12;": "½",
        "&frac34;": "¾",
        "&iquest;": "¿",
        "&times;": "×",
        "&divide;": "÷",
        "&Agrave;": "À",
        "&Aacute;": "Á",
        "&Acirc;": "Â",
        "&Atilde;": "Ã",
        "&Auml;": "Ä",
        "&Aring;": "Å",
        "&AElig;": "Æ",
        "&Ccedil;": "Ç",
        "&Egrave;": "È",
        "&Eacute;": "É",
        "&Ecirc;": "Ê",
        "&Euml;": "Ë",
        "&Igrave;": "Ì",
        "&Iacute;": "Í",
        "&Icirc;": "Î",
        "&Iuml;": "Ï",
        "&ETH;": "Ð",
        "&Ntilde;": "Ñ",
        "&Ograve;": "Ò",
        "&Oacute;": "Ó",
        "&Ocirc;": "Ô",
        "&Otilde;": "Õ",
        "&Ouml;": "Ö",
        "&Oslash;": "Ø",
        "&Ugrave;": "Ù",
        "&Uacute;": "Ú",
        "&Ucirc;": "Û",
        "&Uuml;": "Ü",
        "&Yacute;": "Ý",
        "&THORN;": "Þ",
        "&szlig;": "ß",
        "&agrave;": "à",
        "&aacute;": "á",
        "&acirc;": "â",
        "&atilde;": "ã",
        "&auml;": "ä",
        "&aring;": "å",
        "&aelig;": "æ",
        "&ccedil;": "ç",
        "&egrave;": "è",
        "&eacute;": "é",
        "&ecirc;": "ê",
        "&euml;": "ë",
        "&igrave;": "ì",
        "&iacute;": "í",
        "&icirc;": "î",
        "&iuml;": "ï",
        "&eth;": "ð",
        "&ntilde;": "ñ",
        "&ograve;": "ò",
        "&oacute;": "ó",
        "&ocirc;": "ô",
        "&otilde;": "õ",
        "&ouml;": "ö",
        "&oslash;": "ø",
        "&ugrave;": "ù",
        "&uacute;": "ú",
        "&ucirc;": "û",
        "&uuml;": "ü",
        "&yacute;": "ý",
        "&thorn;": "þ",
        "&yuml;": "ÿ",
        "&OElig;": "Œ",
        "&oelig;": "œ",
        "&Scaron;": "Š",
        "&scaron;": "š",
        "&Yuml;": "Ÿ",
        "&circ;": "ˆ",
        "&tilde;": "˜",
        "&ensp;": " ",
        "&emsp;": " ",
        "&thinsp;": " ",
        "&zwnj;": " ",
        "&zwj;": " ",
        "&lrm;": " ",
        "&rlm;": " ",
        "&ndash;": "–",
        "&mdash;": "—",
        "&lsquo;": "‘",
        "&rsquo;": "’",
        "&sbquo;": "‚",
        "&ldquo;": "“",
        "&rdquo;": "”",
        "&bdquo;": "„",
        "&dagger;": "†",
        "&Dagger;": "‡",
        "&hellip;": "…",
        "&permil;": "‰",
        "&lsaquo;": "‹",
        "&rsaquo;": "›",
        "&euro;": "€",
    }
    text = re.sub(removables_pattern, "", text)
    text = re.sub(whitespace_pattern, " ", text)
    text = re.sub(line_break_pattern, "\n", text)
    text = re.sub(new_line_pattern, "\n\n", text)
    # <a href="URL">NAME</a> -> NAME (URL)
    text = re.sub(link_pattern, link_replacement, text)
    # remove the rest html tags
    text = re.sub(html_tag_pattern, "", text)

    # &<word-based>; -> <special symbol>
    for k, v in html_entities.items():
        text = text.replace(k, v)
    # &#<unicode-number-based>; -> <special symbol>
    text = re.sub(coded_entity_pattern, to_utf8, text)
    # remove the rest html entities
    text = re.sub(html_entity_pattern, "", text)
    text = force_text(text)
    return text


def strip_html(text):
    def fixup(m):
        text = m.group(0)
        if text[:1] == "<":
            return ""  # ignore tags
        if text[:2] == "&#":
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        elif text[:1] == "&":
            try:
                from html.entities import entitydefs
            except ImportError:
                from htmlentitydefs import entitydefs

            entity = entitydefs.get(text[1:-1])
            if entity:
                if entity[:2] == "&#":
                    try:
                        return unichr(int(entity[2:-1]))
                    except ValueError:
                        pass
                else:
                    return force_text(entity, encoding="iso-8859-1")
        return text  # leave as is

    return re.sub("(?s)<[^>]*>|&#?\w+;", fixup, text)


def get_related_queryset(model, field_name):
    """
    Get the queryset for the choices of the field in a model
    Example:
        types = get_related_queryset(Person, "individual_type")
    """
    f = model._meta.get_field(field_name)
    try:
        qs = f.related_model.objects.complex_filter(f.remote_field.limit_choices_to)
    except AttributeError:
        qs = f.rel.to._default_manager.complex_filter(f.rel.limit_choices_to)
    return qs


class XChoiceList(list):
    """ List of choices.
    Takes a function, queryset or list as a parameter and returns the list only when iterating,
    """

    def __init__(self, sequence=None, null_choice_text="-" * 9):
        super(XChoiceList, self).__init__()
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
        return force_text(self._get_list())

    def __unicode__(self):
        return force_text(self._get_list())

    def __repr__(self):
        return repr(self._get_list())

    def _get_list(self):
        if hasattr(self.sequence, "model"):
            result = [("", self.null_choice_text)] + [
                (
                    el.id,
                    el.get_title() if hasattr(el, "get_title") else force_text(el),
                )
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


class ExtendedJSONEncoder(json.JSONEncoder):
    def default(self, o, markers=None):
        if isinstance(o, models.Model):
            return o.__dict__
        if isinstance(o, datetime):
            return {
                "year": o.year,
                "month": o.month,
                "day": o.day,
                "hour": o.hour,
                "minute": o.minute,
                "second": o.second,
                "microsecond": o.microsecond,
            }
        if isinstance(o, time):
            return {
                "hour": o.hour,
                "minute": o.minute,
                "second": o.second,
                "microsecond": o.microsecond,
            }
        if isinstance(o, Decimal):
            return str(o)
        if hasattr(o, "path"):  # FileObject
            return o.path
        if type(o).__name__ == "ModelState":
            return None
        return json.JSONEncoder.default(self, o)


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
    app_path_bits = apps.get_app_config(app_name).models_module.__name__.split(".")[:-1]
    module_path = ".".join(app_path_bits + path_bits)
    m = __import__(module_path, globals(), locals(), "*")
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
    # ret_var = path_bits.pop()
    app_path_bits = apps.get_app_config(app_name).models_module.__name__.split(".")[:-1]
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
    from django.db import connection

    return model._meta.db_table in connection.introspection.table_names()


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
    for line in value.split("\n"):
        words.extend(line.split(" "))
        words.append("\n")
        length += 1
        if len(words) > length:
            break

    # remove last linefeed
    words.pop()
    length -= 1

    if len(words) > length:
        words = words[:length]
        if not words[-1].endswith("..."):
            words.append("...")
    return " ".join(words).replace(" \n ", "\n")


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


def smart_truncate(text, length=100, suffix="..."):
    """
    Truncates `text`, on a word boundary, as close to
    the target length it can come.    
    """
    slen = len(suffix)
    pattern = r"^(.{0,%d}\S)\s+\S+" % (length - slen - 1)
    if len(text) > length:
        match = re.match(pattern, text)
        if match:
            length0 = match.end(0)
            length1 = match.end(1)
            if abs(length0 + slen - length) < abs(length1 + slen - length):
                return match.group(0) + suffix
            else:
                return match.group(1) + suffix
    return text


def get_unused_languages(exclude=("id",)):
    """ get a list of language codes which are unused (except Indonesian)"""
    from django.conf import global_settings

    installed_languages = [lang[0] for lang in settings.LANGUAGES]
    available_languages = [
        lang[0] for lang in global_settings.LANGUAGES if len(lang[0]) == 2
    ]
    unused_languages = [
        lang
        for lang in available_languages
        if lang not in installed_languages and lang not in exclude
    ]
    return unused_languages
