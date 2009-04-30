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
"""Adapter implementation for generating pdf reports of MiscPhysical"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.component import adapts

# ict_ok.org imports
from org.ict_ok.components.misc_physical.interfaces import IMiscPhysical
from org.ict_ok.components.misc_physical.misc_physical import MiscPhysical
from org.ict_ok.components.misc_physical.browser.misc_physical import \
    MiscPhysicalDetails
from org.ict_ok.components.supernode.adapter.rpt_pdf import \
    RptPdf as ParentRptPdf
from org.ict_ok.admin_utils.reports.interfaces import IRptPdf


class RptPdf(ParentRptPdf):
    """adapter implementation of miscellaneous physical component -> PDF Report
    """

    implements(IRptPdf)
    adapts(IMiscPhysical)
    factory = MiscPhysical
    omitFields = MiscPhysicalDetails.omit_viewfields
