#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
The original file is improved by adding the containing directory to python search path. This small improvement enables executing the script without cd to it.
Examples:
   python path/to/myproject/manage.py shell
   ./path/to/myproject/manage.py shell
   /Library/myproject/manage.py shell
   /Library/myproject/manage.py shell --settings=other.settings
It's useful for running sheduled tasks which can be integrated into django management commands
"""
import os
import sys
import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)

from django.core.management import execute_manager

sys.path.insert(0, os.path.dirname(__file__))

if __name__ == "__main__":
    try:
        import settings
    except ImportError:
        import sys
        sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % __file__)
        sys.exit(1)
    execute_manager(settings)

