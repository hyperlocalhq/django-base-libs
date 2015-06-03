# -*- coding: utf-8 -*-
COMPRESS = True
COMPRESS_AUTO = False
COMPRESS_VERSION = False

### CSS COMPRESSION ###

COMPRESS_CSS_FILTERS = [
    "compress.filters.csstidy.CSSTidyFilter",
    "compress.filters.yui.YUICompressorFilter",
    ]

COMPRESS_CSS = {}
COMPRESS_JETSON_CSS = {}

### JAVASCRIPT COMPRESSION ###

COMPRESS_JS_FILTERS = [
    "compress.filters.jsmin.JSMinFilter",
    "compress.filters.yui.YUICompressorFilter",
    ]

COMPRESS_JS = {}
COMPRESS_JETSON_JS = {}

### COMPRESSION FILTER SETTINGS ###

CSSTIDY_BINARY = os.path.join(EXTERNAL_LIBS_PATH, "csstidy")
CSSTIDY_ARGUMENTS = "--template=highest --merge_selectors=0"

COMPRESS_YUI_BINARY = "java -jar %s" % os.path.join(EXTERNAL_LIBS_PATH, "yuicompressor-2.4.2.jar")
COMPRESS_YUI_CSS_ARGUMENTS = "--line-break 0 --charset utf8"
COMPRESS_YUI_JS_ARGUMENTS = "--line-break 0 --charset utf8 --nomunge"

