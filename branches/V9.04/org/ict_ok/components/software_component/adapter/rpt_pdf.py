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
"""Adapter implementation for generating pdf reports of Outlet"""

__version__ = "$Id: rpt_pdf.py 394 2009-01-06 15:12:30Z markusleist $"

# python imports

# zope imports
from zope.interface import implements
from zope.component import adapts

# ict_ok.org imports
from org.ict_ok.components.software_component.interfaces import \
    ISoftwareComponent
from org.ict_ok.components.software_component.software_component import \
    SoftwareComponent
from org.ict_ok.components.software_component.browser.software_component \
    import SoftwareComponentDetails
from org.ict_ok.components.supernode.adapter.rpt_pdf import \
     RptPdf as ParentRptPdf
from org.ict_ok.admin_utils.reports.interfaces import IRptPdf


# ict_ok.org imports
class RptPdf(ParentRptPdf):
    """adapter implementation of An software instance -> PDF Report
    """

    implements(IRptPdf)
    adapts(ISoftwareComponent)
    factory = SoftwareComponent
    omitFields = SoftwareComponentDetails.omit_viewfields
