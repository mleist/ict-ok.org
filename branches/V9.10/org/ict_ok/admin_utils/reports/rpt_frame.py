# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# no_pylint: disable-msg=W0232
#
"""rpt_frame module 

frame-class for ict-ok.org reporting 
"""

__version__ = "$Id$"

# phython imports

# zope imports

# reportlab imports
from reportlab.platypus import Frame

# ict-ok.org imports

class RptFrame(Frame):
    def __init__(self, x1, y1, width, height,
                 leftPadding=0, bottomPadding=0,
                 rightPadding=0, topPadding=0,
                 id=None, showBoundary=0,
                 overlapAttachedSpace=None,_debug=None):
        Frame.__init__(self, x1, y1, width,height, leftPadding,
                       bottomPadding, rightPadding, topPadding,
                       id, showBoundary, overlapAttachedSpace,
                       _debug)
