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
"""rpt_page module 

page-class for ict-ok.org reporting 
"""

__version__ = "$Id: $"

# phython imports

# zope imports
from zope.component import getUtility

# reportlab imports
from reportlab.lib.units import mm, cm
from reportlab.lib.pagesizes import A4
from reportlab.platypus import PageTemplate

# ict-ok.org imports
from org.ict_ok.admin_utils.reports.rpt_color import CMYK_RPT1
from org.ict_ok.admin_utils.reports.interfaces import IAdmUtilReports

class RptPageTemplate(PageTemplate):
    def afterDrawPage(self, canv, doc):
        admUtilReports = getUtility(IAdmUtilReports)
        canv.saveState()
        canv.setStrokeColor(CMYK_RPT1)
        canv.setFillColor(CMYK_RPT1)
        canv.rect(65 * mm, A4[1] - 18.75 * mm,
                  14 * cm, 1 * cm, fill=1)
        if admUtilReports.logoFile1 is not None:
            canv.drawImage(admUtilReports.logoFile1, 20 * mm, A4[1]-18.75 * mm, width=4 * cm, height=1 * cm)
        canv.setFont('Helvetica', 12)
        canv.setStrokeColorRGB(1, 1, 1)
        canv.setFillColorRGB(1, 1, 1)
        if doc.volumeNo:
            canv.drawRightString(200 * mm, 281.5 * mm, doc.volumeNo)
        if doc.firstPageTitle:
            canv.drawRightString(185 * mm, 281.5 * mm, doc.firstPageTitle)
            doc.firstPageTitle = None
        elif doc.lastPageTitle:
            canv.drawRightString(185 * mm, 281.5 * mm, doc.lastPageTitle)
        canv.setStrokeColorRGB(0, 0, 0)
        canv.setFillColorRGB(0, 0, 0)
        canv.setFont('Helvetica', 12)
        if doc.volumeNo:
            tmpStrgPageNo = "%s - %d" % (doc.volumeNo, doc.page)
        else:
            tmpStrgPageNo = "%d" % (doc.page)
        canv.drawRightString(185 * mm, 12.5 * mm, tmpStrgPageNo)
        canv.setFont('Helvetica', 7)
        if doc.authorName:
            canv.drawString(50 * mm, 12.5 * mm, doc.authorName)
        if doc.versionStr:
            canv.drawString(50 * mm, 9.5 * mm, doc.versionStr)
        canv.restoreState()
