#!/usr/bin/env sh
python manage.py dumpdata \
    --indent=4 \
    cms \
    richtext \
    filebrowser_image \
    gmap \
    headline \
    editorial \
    djangocms_column \
    djangocms_file \
    djangocms_flash \
    djangocms_inherit \
    djangocms_link \
    djangocms_style \
    djangocms_teaser \
    djangocms_video
