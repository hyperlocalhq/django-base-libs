# -*- coding: utf-8 -*-
import re
from django.db import models
from django import template
from django.apps import apps
from django.template import TemplateSyntaxError

from base_libs.utils.misc import truncwords
from base_libs.models.base_libs_settings import STATUS_CODE_PUBLISHED

register = template.Library()

### TAGS ### 


class TagCloudForBlogNode(template.Node):
    def __init__(self, blog, context_var, **kwargs):
        self.blog = blog
        self.context_var = context_var
        self.kwargs = kwargs

    def render(self, context):
        Post = apps.get_model("blog", "Post")
        Tag = apps.get_model("tagging", "Tag")
        self.kwargs['filters'] = {
            'blog': template.resolve_variable(self.blog, context),
            'status': STATUS_CODE_PUBLISHED,
        }
        context[self.context_var] = sorted(Tag.objects.cloud_for_model(
            Post,
            **self.kwargs
            ), lambda x, y: int(y.count - x.count))
        return ''

def do_tag_cloud_for_blog(parser, token):
    """
    Retrieves a list of ``Tag`` objects for a given model, with tag
    cloud attributes set, and stores them in a context variable.

    Usage::

       {% tag_cloud_for_blog [blog] as [varname] %}

    Extended usage::

       {% tag_cloud_for_blog [blog] as [varname] with [options] %}

    Extra options can be provided after an optional ``with`` argument,
    with each option being specified in ``[name]=[value]`` format. Valid
    extra options are:

       ``steps``
          Integer. Defines the range of font sizes.

       ``min_count``
          Integer. Defines the minimum number of times a tag must have
          been used to appear in the cloud.

       ``distribution``
          One of ``linear`` or ``log``. Defines the font-size
          distribution algorithm to use when generating the tag cloud.

    Examples::

       {% tag_cloud_for_blog blog as blog_tags %}
       {% tag_cloud_for_blog blog as blog_tags with steps=9 min_count=3 distribution=log %}

    """
    from tagging.utils import LINEAR, LOGARITHMIC
    bits = token.contents.split()
    len_bits = len(bits)
    if len_bits != 4 and len_bits not in range(6, 9):
        raise TemplateSyntaxError(_('%s tag requires either three or between five and seven arguments') % bits[0])
    if bits[2] != 'as':
        raise TemplateSyntaxError(_("second argument to %s tag must be 'as'") % bits[0])
    kwargs = {}
    if len_bits > 5:
        if bits[4] != 'with':
            raise TemplateSyntaxError(_("if given, fourth argument to %s tag must be 'with'") % bits[0])
        for i in range(5, len_bits):
            try:
                name, value = bits[i].split('=')
                if name == 'steps' or name == 'min_count':
                    try:
                        kwargs[str(name)] = int(value)
                    except ValueError:
                        raise TemplateSyntaxError(_("%(tag)s tag's '%(option)s' option was not a valid integer: '%(value)s'") % {
                            'tag': bits[0],
                            'option': name,
                            'value': value,
                        })
                elif name == 'distribution':
                    if value in ['linear', 'log']:
                        kwargs[str(name)] = {'linear': LINEAR, 'log': LOGARITHMIC}[value]
                    else:
                        raise TemplateSyntaxError(_("%(tag)s tag's '%(option)s' option was not a valid choice: '%(value)s'") % {
                            'tag': bits[0],
                            'option': name,
                            'value': value,
                        })
                else:
                    raise TemplateSyntaxError(_("%(tag)s tag was given an invalid option: '%(option)s'") % {
                        'tag': bits[0],
                        'option': name,
                    })
            except ValueError:
                raise TemplateSyntaxError(_("%(tag)s tag was given a badly formatted option: '%(option)s'") % {
                    'tag': bits[0],
                    'option': bits[i],
                })
    return TagCloudForBlogNode(bits[1], bits[3], **kwargs)

register.tag('tag_cloud_for_blog', do_tag_cloud_for_blog)


### FILTERS ### 

def markup2html(value, arg=None):
    
    """
    Converts a string in Markdown or ReST to HTML using
    the appropriate filter. Optionally truncates
    the string after arg words.

    arg:
      Number of words to truncate after (ex:80)
    """

    if value.startswith('..'):
        return rest2html(value, arg)
    else:
        return markdown2html(value, arg)
    
markup2html = register.filter(markup2html)      
    
def markdown2html(value, arg=None):
    
    """
    Converts a string to HTML using the markdown
    filter, with optional processing arguments.

    arg:
      Number of words to truncate after (ex:80)
    """

    def clean(s):
        # remove images
        s = re.sub(r'!\[[^\]]*\]\([^\)]+\)(\s+\n)?', r'', s)
        # remove links
        s = re.sub(r'\[([^\]]+)\]\([^\)]+\)?', r'\1', s)
        # remove header chars
        s = re.sub(r'(?m)^#*', r'', s)
        # remove formatting
        s = re.sub(r'(\*|_|`)(.*?)\1', r'\2', s)
        return s
    
    if not isinstance(value, basestring):
        value = str(value)

    # truncate it *before* markdown so tags are closed properly
    if arg:
        try:
            length = int(arg)
        except ValueError:
            return value
        # don't format it - just return bare text
        return truncwords(clean(value), length)

    #RS12042007 change begin 
    #    at now, we do not convert to markdown!!!!
    return value
    #RS12042007 change end
    
markdown2html = register.filter(markdown2html)           

def rest2html(value, arg=None):
    
    """
    Converts a string to HTML using the restructuredtext
    filter, with optional processing arguments.

    arg:
      Number of words to truncate after (ex:80)
    """

    def clean(s):
        # remove directives
        s = re.sub(r'(?ms)^\.\.\s+.*?(\r|\n|\r\n)\1', r'', s)
        # clean up formatting
        s = re.sub(r'(\*{1,2}|`)(.*?)\1', r'\2', s)
        # clean up links
        s = re.sub(r'(\w+)_(\W)', r'\1\2', s)
        return s
    
    if not isinstance(value, basestring):
        value = str(value)
        
    # truncate it *before* markdown so tags are closed properly
    if arg:
        try:
            length = int(arg)
        except ValueError:
            return value
        # don't format it - just return bare text
        return truncwords(clean(value), length)

    # conver to markdown
    try:
        from docutils.core import publish_parts
    except ImportError:
        #from django.conf import settings
        #if settings.DEBUG:
        #    raise template.TemplateSyntaxError, \
        #          "Error in {% rest2html %} filter: " + \
        #          "The Python docutils library isn't installed."
        return value
    else:
        settings_overrides = {'initial_header_level': 2}
        parts = publish_parts(source=value, writer_name='html4css1',
                              settings_overrides=settings_overrides)
        return parts['fragment']

rest2html = register.filter(rest2html)           
truncwords = register.filter(truncwords)           

string_rule = r'(\'[^\']*\'|"[^"]*")'
oldc_comment_rule = r'(/\*[^*]*\*+([^/][^*]*\*+)*/)'
newc_comment_rule = r'((//[^\n]*\n)|(/\*[^*]*\*+([^/][^*]*\*+)*/))'
shell_comment_rule = r'(#[^\n]*)\n'

# REALLY the way you want to do this is to walk through te string and
# apply each re pattern to the remainder (starting with the whole thing)
# and then the one that matches the earliest should be applied and then
# you should continue at the end. then the order doesn't matter and you
# won't have problems of matching string within comment or keyword within
# string et.c
# TODO
# - convert this back to dicts!
# - make inner loop like outer loop but use earliest match approach
SYNTAX_RULES = {
    'c': {
    'comment': newc_comment_rule,
    'string': string_rule,
    'preprocessor': shell_comment_rule,
    'keyword': r'\b(bool|break|byte|case|char|const|continue|default|do|double|else|enum|extern|false|float|for|goto|if|int|long|null|return|short|sizeof|static|struct|switch|true|uint|ulong|ushort|volatile|void|while)\b',
    },

    'cmd': {
    'comment': r'\b([Rr][Ee][Mm]( [^\n]*)?)\n',
    'string': string_rule,
    'keyword': r'\b(assoc|at|attrib|break|cacls|call|cd|chcp|chdir|chkdsk|chkntfs|cls|color|comp|compact|convert|copy|date|del|dir|diskcomp|diskcopy|doskey|echo|endlocal|erase|exit|fc|find|findstr|for|format|ftype|goto|graftabl|help|if|label|md|mkdir|mode|more|move|path|pause|popd|print|prompt|pushd|rd|recover|ren|rename|replace|rmdir|set|setlocal|shift|sort|start|subst|time|title|tree|type|ver|verify|vol|xcopy)\b',
    },

    'csharp': {
    'comment': newc_comment_rule,
    'string': string_rule,
    'preprocessor': shell_comment_rule,
    'keyword': r'\b(abstract|as|base|bool|break|byte|case|catch|char|checked|class|const|continue|decimal|default|delegate|do|double|else|enum|event|explicit|extern|false|finally|fixed|float|for|foreach|goto|if|implicit|in|int|interface|internal|is|lock|long|namespace|new|null|object|operator|out|override|params|private|protected|public|readonly|ref|return|sbyte|sealed|short|sizeof|stackalloc|static|string|struct|switch|this|throw|true|try|typeof|uint|ulong|unchecked|unsafe|ushort|using|virtual|volatile|void|while)\b',
    },

    'css': {
    'comment': oldc_comment_rule,
    'keyword': r'(@\w[\w\s]*)',
    'selector': r'([-:#\w\[\.][^{};>]*)(?={)',
    'property': r'([\w-]+)(?=\s*:)',
    'unit': r'[0-9\.]+(em|en|px|%|pt)\b',
    'url': r'(url\([^\)]*\))',
    },
    
    'html': {
    'comment': r'(<!\s*(--([^-]|[\r\n]|-[^-])*--\s*)>)',
    'string': string_rule,
    'element': r'<\/?([a-zA-Z]+)\s?',
    'attribute': r'\b([a-zA-Z-:]+)=',
    'doctype': r'(<!DOCTYPE([^>])*>)',
    },
    
    'javascript': {
    'comment': newc_comment_rule,
    'string': string_rule,
    'global': r'\b(toString|valueOf|window|element|prototype|constructor|document|escape|unescape|parseInt|parseFloat|setTimeout|clearTimeout|setInterval|clearInterval|NaN|isNaN|Infinity)\b',
    'keyword': r'\b(arguments|break|case|continue|default|delete|do|else|false|for|function|if|in|instanceof|new|null|return|switch|this|true|typeof|var|void|while|with)\b',
    },
    
    'python': {
    'comment': shell_comment_rule,
    # from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/475109
    'string': r"""[uU]?[rR]?('''(?:[^']|\\'|'{1,2}(?!'))*'''|'(?:[^']|\\')*'(?!')|""" + r'''"""(?:[^"]|\\"|"{1,2}(?!"))*"""|"(?:[^"]|\\")*"(?!"))''',
    'keyword': r'\b(and|assert|break|class|continue|def|del|elif|else|except|exec|finally|for|from|global|if|import|in|is|lambda|not|or|pass|print|raise|return|try|while|yield|None|True|False)\b',
    },
    
    'sql': {
    'comment': r'(--[^\n]*\n)|(/\*[^*]*\*+([^/][^*]*\*+)*/)',
    'string': r"('[^']*')",
    'keyword': r'\b(abs|alter|and|any|avg|backup|begin|between|binary|bit|break|bulk|case|char|charindex|close|coalesce|contains|count|create|cursor|database|datalength|dateadd|datediff|datename|datepart|day|decimal|declare|delete|drop|dump|else|end|exec|execute|exists|fetch|float|from|getdate|go|goto|grant|group by|having|identity|if|image|in|insert|is|left|len|like|max|not|null|numeric|open|or|order by|print|raiserror|real|restore|return|rollback|round|select|set|smalldatetime|smallint|smallmoney|stdev|substring|sum|table|text|timestamp|trans|transaction|trigger|truncate|union|update|use|user|where|while)\b',
    },
    
    }

class CodeHighlighter(object):
    
    def run(self, doc):
        """
        Search the DOM for all code blocks and highligh each
        block based on the language for that block.
        """
        
        def findCodeBlock(node=None, indent=0):
            """
            Find a code block. Markdown stores these
            as <pre><code>...</code></pre>. We also require
            the CSS class attribute to indicate the language
            rules for code hilighting, but Markdown hasn't processed
            the {@attr=value} markup yet so we need to search for
            the pattern within the text of the <code/> node.
            """
            try:
                if node.type == 'element' and node.nodeName == 'pre':
                    code = node.childNodes[0]
                    if code.type == 'element' and code.nodeName == 'code':
                        text = code.childNodes[0]
                        m = text.attrRegExp.search(text.value)
                        if m and m.group(1) == 'class':
                            return True
            except:
                return False
                    
        code_blocks = doc.find(findCodeBlock)
        if code_blocks:
            for pre in code_blocks:
                code = pre.childNodes[0]
                text = code.childNodes[0]
                
                # Similar to findCodeBlock above, we need to search for
                # the class attribute markup in the text since it hasn't
                # been processed yet
                match = text.attrRegExp.search(text.value)
                # strip out the attribute markup from the text so we
                # don't highlight it
                source = text.value[:match.start(0)] + text.value[match.end(0):]
                highlight = self.highlight_block(doc, source, match.group(2))
                pre.replaceChild(code, highlight)
                
    def highlight_block(self, doc, text, language):
        code = doc.createElement('code')
        code.setAttribute('class', language)
        while text:
            # find the rule that matches first so we don't have odd
            # situations like matching a string within a comment
            first = None
            for key, rule in SYNTAX_RULES.get(language, {}).items():
                try:
                    match = re.search(rule, text)
                    if match and \
                           (not first
                            or match.start(1) < first['match'].start(1)):
                        first = {'match': match, 'key': key}
                except:
                    print 'key:', key, ' rule:', rule
                    raise
            
            if first:
                # append a text node for the piece before the match
                code.appendChild(doc.createTextNode(text[:first['match'].start(1)]))
                # create and append a span node for the match with
                # the CSS class of the language element (keyword, comment, etc.)
                span = doc.createElement('span', first['match'].group(1))
                span.setAttribute('class', first['key'])
                code.appendChild(span)
                # continue with the rest of the text
                text = text[first['match'].end(1):]
            else:
                # no pattern found, add the remaining text node
                code.appendChild(doc.createTextNode(text))
                text = None
                
        return code

