# -*- coding: utf-8 -*-
PIPELINE = True
PIPELINE_AUTO = False

### CSS COMPRESSION ###

PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yui.YUICompressor'

PIPELINE_CSS = {}
COMPRESS_JETSON_CSS = {}

### JAVASCRIPT COMPRESSION ###

PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yui.YUICompressor'

PIPELINE_JS = {}
COMPRESS_JETSON_JS = {}

### COMPRESSION FILTER SETTINGS ###

PIPELINE_YUI_BINARY = "java -jar %s" % os.path.join(EXTERNAL_LIBS_PATH, "yuicompressor-2.4.2.jar")
PIPELINE_YUI_CSS_ARGUMENTS = "--line-break 0 --charset utf8"
PIPELINE_YUI_JS_ARGUMENTS = "--line-break 0 --charset utf8 --nomunge"

