# -*- coding: utf-8 -*-
FILEBROWSER_MEDIA_ROOT = MEDIA_ROOT
FILEBROWSER_DIRECTORY = ""

UPLOADS_ROOT = MEDIA_ROOT

FILEBROWSER_MEDIA_URL = UPLOADS_URL = "/uploads/"
FILEBROWSER_VERSIONS_BASEDIR = "__versions__"

FILEBROWSER_VERSIONS = {
    'fb_thumb': {'verbose_name': 'Admin Thumbnail', 'width': 60, 'height': 60, 'opts': 'crop upscale'},
}

FILEBROWSER_ADMIN_VERSIONS = []
FILEBROWSER_ADMIN_THUMBNAIL = 'fb_thumb'

FILEBROWSER_EXTENSIONS = {
    'Folder': [''],
    'Image': ['.jpg','.jpeg','.gif','.png','.tif','.tiff'],
    'Video': ['.mov','.wmv','.mpeg','.mpg','.avi','.rm'],
    'Document': ['.pdf','.doc','.docx','.rtf','.txt',
        '.xls','.xlsx','.csv','.ppt','.pptx',
        ],
    'Audio': ['.mp3','.mp4','.wav','.aiff','.midi','.m4p'],
    'Code': ['.html','.py','.js','.css'],
    'Archive': ['.zip','.rar','.tar','.gz'],
}

FILEBROWSER_SELECT_FORMATS = {
    'File': ['Folder','Document',],
    'Image': ['Image'],
    'Media': ['Video','Sound'],
    'Document': ['Document'],
    # for TinyMCE we also have to define lower-case items
    'image': ['Image'],
    'file': ['Folder','Image','Document',],
}

_extension_list = []
for exts in FILEBROWSER_EXTENSIONS.values():
    _extension_list += exts
FILEBROWSER_EXCLUDE = (
    r'_(%(exts)s)_.*_q\d{1,3}\.(%(exts)s)' % {'exts': ('|'.join(_extension_list))},
    r'_cache',
    r'__versions__',
    )

FILEBROWSER_SAVE_FULL_URL = False

FILEBROWSER_URL_TINYMCE = STATIC_URL + "grappelli/tinymce/jscripts/tiny_mce/"
FILEBROWSER_PATH_TINYMCE = STATIC_URL + "grappelli/tinymce/jscripts/tiny_mce/"
FILEBROWSER_URL_FILEBROWSER_MEDIA = STATIC_URL + 'filebrowser/'

