# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: rpt_pdf.py_cog 506 2009-04-30 14:24:56Z markusleist $
#
# pylint: disable-msg=E1101,E0611,W0142
#
"""Adapter implementation for generating pdf reports of Organization"""

__version__ = "$Id: rpt_pdf.py_cog 506 2009-04-30 14:24:56Z markusleist $"

# python imports

# zope imports
from zope.interface import implements
from zope.component import adapts

# z3c imports
from z3c.form import field

# ict_ok.org imports
from org.ict_ok.components.organization.interfaces import IOrganization
from org.ict_ok.components.organization.organization import Organization
from org.ict_ok.components.organization.browser.organization import \
    OrganizationDetails
from org.ict_ok.components.contact_item.adapter.rpt_pdf import \
     RptPdf as ParentRptPdf
from org.ict_ok.admin_utils.reports.interfaces import IRptPdf


class RptPdf(ParentRptPdf):
    """adapter implementation of Organization -> PDF Report
    """

    implements(IRptPdf)
    adapts(IOrganization)
    factory = Organization
    omitFields = ParentRptPdf.omitFields + []

