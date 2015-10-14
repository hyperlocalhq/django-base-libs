# -*- coding: UTF-8 -*-
import os

from django.db import models

# execute guerrilla patches
patches_dir = os.path.join(os.path.dirname(__file__), "guerrilla_patches")
for filename in os.listdir(patches_dir):
    if os.path.splitext(filename)[1] == ".py":
        execfile(os.path.join(patches_dir, filename))
