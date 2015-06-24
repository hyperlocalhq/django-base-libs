# -*- coding: UTF-8 -*-
import os

from django.db import models

# execute guerrilla patches
patches_dir = os.path.join(os.path.dirname(__file__), "guerrilla_patches")
for filename in os.listdir(patches_dir):
    if os.path.splitext(filename)[1] == ".py":
        execfile(os.path.join(patches_dir, filename))

from filebrowser.fields import FileBrowseField

try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    add_introspection_rules(
        [(
            [FileBrowseField],  # Class(es) these apply to
            [],                 # Positional arguments (not used)
            {                   # Keyword argument
                "directory": ["directory", {"default": ""}],
                "extensions": ["extensions", {"default": ""}],
                "format": ["format", {"default": ""}],
            },
            ),],
        ["^filebrowser\.fields\.FileBrowseField"],
        )

