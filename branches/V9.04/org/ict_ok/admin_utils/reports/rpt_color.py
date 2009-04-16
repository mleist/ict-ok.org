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
"""rpt_color module 

color-class for ict-ok.org reporting 
"""

__version__ = "$Id: $"

# zope imports
from zope.component import getUtility

# reportlab imports
from reportlab.lib import colors

# ict-ok.org imports
from org.ict_ok.admin_utils.reports.interfaces import IAdmUtilReports

#CMYK_RPT1=colors.CMYKColor(1.0, 0.49, 0.612, 0.0)

def getColor1():
    admUtilReports = getUtility(IAdmUtilReports, name='AdmUtilReports')
    if admUtilReports.color1 is not None:
        rString = admUtilReports.color1[1:3]
        gString = admUtilReports.color1[3:5]
        bString = admUtilReports.color1[5:7]
        rValue = float(int(rString, 16))/256.0
        gValue = float(int(gString, 16))/256.0
        bValue = float(int(bString, 16))/256.0
        cmyk_tuple = colors.rgb2cmyk(rValue, gValue, bValue)
        return colors.CMYKColor(*cmyk_tuple)
    else:
        return colors.CMYKColor(1.0, 0.49, 0.612, 0.0)