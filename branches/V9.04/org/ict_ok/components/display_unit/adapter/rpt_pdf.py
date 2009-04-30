# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0142
#
"""Adapter implementation for generating pdf reports of DisplayUnit"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.component import adapts

# ict_ok.org imports
from org.ict_ok.components.display_unit.interfaces import IDisplayUnit
from org.ict_ok.components.display_unit.display_unit import DisplayUnit
from org.ict_ok.components.display_unit.browser.display_unit import \
    DisplayUnitDetails
from org.ict_ok.components.supernode.adapter.rpt_pdf import \
    RptPdf as ParentRptPdf
from org.ict_ok.admin_utils.reports.interfaces import IRptPdf


class RptPdf(ParentRptPdf):
    """adapter implementation of Display unit instance -> PDF Report
    """

    implements(IRptPdf)
    adapts(IDisplayUnit)
    factory = DisplayUnit
    omitFields = DisplayUnitDetails.omit_viewfields
