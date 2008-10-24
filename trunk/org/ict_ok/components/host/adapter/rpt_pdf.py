# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0142
#
"""Adapter implementation for generating graphviz-dot configuration
"""


__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.component import adapts

# z3c imports
from z3c.form import field

# ict_ok.org imports
from org.ict_ok.components.host.interfaces import IHost
from org.ict_ok.components.supernode.adapter.rpt_pdf import \
     RptPdf as ParentRptPdf
from org.ict_ok.admin_utils.reports.interfaces import IRptPdf


class RptPdf(ParentRptPdf):
    """adapter implementation of latency -> PDF Report
    """

    implements(IRptPdf)
    adapts(IHost)

    def getReportFields(self):
        """
        """
        from org.ict_ok.components.host.browser.host import HostDetails
        omitField = [
            'snmpVersion',
            'snmpPort',
            'snmpReadCommunity',
            'snmpWriteCommunity',
            'url',
            'url_type',
            'url_authname',
            'url_authpasswd',
            'console',
            'genNagios',
        ]
        omitField.extend(HostDetails.omit_viewfields)
        return field.Fields(IHost).omit(*omitField)

