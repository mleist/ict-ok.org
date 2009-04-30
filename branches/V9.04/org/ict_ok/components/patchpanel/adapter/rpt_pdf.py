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
"""Adapter implementation for generating pdf reports of PatchPanel"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.component import adapts

# ict_ok.org imports
from org.ict_ok.components.patchpanel.interfaces import IPatchPanel
from org.ict_ok.components.patchpanel.patchpanel import PatchPanel
from org.ict_ok.components.patchpanel.browser.patchpanel import \
    PatchPanelDetails
from org.ict_ok.components.supernode.adapter.rpt_pdf import \
    RptPdf as ParentRptPdf
from org.ict_ok.admin_utils.reports.interfaces import IRptPdf


class RptPdf(ParentRptPdf):
    """adapter implementation of Patch panel -> PDF Report
    """

    implements(IRptPdf)
    adapts(IPatchPanel)
    factory = PatchPanel
    omitFields = PatchPanelDetails.omit_viewfields
