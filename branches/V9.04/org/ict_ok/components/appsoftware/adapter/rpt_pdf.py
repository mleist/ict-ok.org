# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: rpt_pdf.py 394 2009-01-06 15:12:30Z markusleist $
#
# pylint: disable-msg=E1101,E0611,W0142
#
"""Adapter implementation for generating pdf reports of ApplicationSoftware"""


__version__ = "$Id: rpt_pdf.py 394 2009-01-06 15:12:30Z markusleist $"

# python imports

# zope imports
from zope.interface import implements
from zope.component import adapts

# z3c imports
from z3c.form import field

# ict_ok.org imports
from org.ict_ok.components.appsoftware.interfaces import IApplicationSoftware
from org.ict_ok.components.supernode.adapter.rpt_pdf import \
     RptPdf as ParentRptPdf
from org.ict_ok.admin_utils.reports.interfaces import IRptPdf


# ict_ok.org imports
class RptPdf(ParentRptPdf):
    """adapter implementation of Application Software Instance -> PDF Report
    """

    implements(IRptPdf)
    adapts(IApplicationSoftware)
    
    def getReportFields(self):
        """
        """
        from org.ict_ok.components.appsoftware.browser.appsoftware import \
             ApplicationSoftwareDetails
        return field.Fields(IApplicationSoftware).omit(\
            *ApplicationSoftwareDetails.omit_viewfields)

