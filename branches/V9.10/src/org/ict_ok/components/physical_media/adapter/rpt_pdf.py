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
"""Adapter implementation for generating pdf reports of PhysicalMedia"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.component import adapts

# z3c imports
from z3c.form import field

# ict_ok.org imports
from org.ict_ok.components.physical_media.interfaces import IPhysicalMedia
from org.ict_ok.components.physical_media.physical_media import PhysicalMedia
from org.ict_ok.components.physical_media.browser.physical_media import \
from org.ict_ok.components.supernode.adapter.rpt_pdf import \
     RptPdf as ParentRptPdf
from org.ict_ok.admin_utils.reports.interfaces import IRptPdf


class RptPdf(ParentRptPdf):
    """adapter implementation of Physical Media -> PDF Report
    """

    implements(IRptPdf)
    adapts(IPhysicalMedia)
    factory = PhysicalMedia
    omitFields = PhysicalMediaDetails.omit_viewfields

