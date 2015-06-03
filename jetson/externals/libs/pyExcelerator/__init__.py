# -*- coding: utf-8 -*-

__rev_id__ = """$Id: __init__.py,v 1.4 2005/05/12 06:51:17 rvk Exp $"""

import sys
if sys.version_info[:2] < (2, 4):
    print >>sys.stderr, "Sorry, pyExcelerator requires Python 2.4 or later"
    sys.exit(1)


from Workbook import Workbook
from Worksheet import Worksheet
from Row import Row
from Column import Column 
from Formatting import Font, Alignment, Borders, Pattern, Protection
from Style import XFStyle 
from ImportXLS import * 

