# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: rpt_pdf.py 394 2009-01-06 15:12:30Z markusleist $
#
# pylint: disable-msg=E1101,E0611,W0142
#
"""Adapter implementation for generating pdf reports of IpAddress"""

__version__ = "$Id: rpt_pdf.py 394 2009-01-06 15:12:30Z markusleist $"

# python imports

# zope imports
from zope.interface import implements
from zope.component import adapts

# ict_ok.org imports
from org.ict_ok.components.ip_address.interfaces import IIpAddress
from org.ict_ok.components.ip_address.ip_address import IpAddress
from org.ict_ok.components.ip_address.browser.ip_address import \
    IpAddressDetails
from org.ict_ok.components.supernode.adapter.rpt_pdf import \
     RptPdf as ParentRptPdf
from org.ict_ok.admin_utils.reports.interfaces import IRptPdf


class RptPdf(ParentRptPdf):
    """adapter implementation of IP address -> PDF Report
    """

    implements(IRptPdf)
    adapts(IIpAddress)
    factory = IpAddress
    omitFields = IpAddressDetails.omit_viewfields
