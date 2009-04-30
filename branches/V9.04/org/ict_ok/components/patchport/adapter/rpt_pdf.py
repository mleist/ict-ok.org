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
"""Adapter implementation for generating pdf reports of PatchPort"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.component import adapts

# ict_ok.org imports
from org.ict_ok.components.patchport.interfaces import IPatchPort
from org.ict_ok.components.patchport.patchport import PatchPort
from org.ict_ok.components.patchport.browser.patchport import PatchPortDetails
from org.ict_ok.components.supernode.adapter.rpt_pdf import \
     RptPdf as ParentRptPdf
from org.ict_ok.admin_utils.reports.interfaces import IRptPdf


class RptPdf(ParentRptPdf):
    """adapter implementation of Patch port -> PDF Report
    """

    implements(IRptPdf)
    adapts(IPatchPort)
    factory = PatchPort
    omitFields = PatchPortDetails.omit_viewfields
