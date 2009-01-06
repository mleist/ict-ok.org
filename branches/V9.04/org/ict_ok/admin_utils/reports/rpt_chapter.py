# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: interfaces.py 350 2008-10-12 09:18:43Z markusleist $
#
# no_pylint: disable-msg=W0232
#
"""rpt_chapter 

Chapter class for ict-ok.org reporting 
"""

__version__ = "$Id: $"

# ict-ok.org imports
from org.ict_ok.admin_utils.reports.rpt_base import RptSuperclass

class RptChapter(RptSuperclass):
    """Chapter class for ict-ok.org reporting 
    """
    def __init__(self):
        """
        constructor of the object
        """
        RptSuperclass.__init__(self)
        self._element_type = "chapter"

    def __str__(self):
        return u""
