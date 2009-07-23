# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: rpt_pdf.py_cog 519 2009-05-12 07:44:37Z markusleist $
#
# pylint: disable-msg=E1101,E0611,W0142
#
"""Adapter implementation for generating pdf reports of InternalAttachment"""

__version__ = "$Id: rpt_pdf.py_cog 519 2009-05-12 07:44:37Z markusleist $"

# python imports

# zope imports
from zope.interface import implements
from zope.component import adapts

# z3c imports
from z3c.form import field

# ict_ok.org imports
from org.ict_ok.components.int_attachment.interfaces import IInternalAttachment
from org.ict_ok.components.int_attachment.int_attachment import InternalAttachment
from org.ict_ok.components.int_attachment.browser.int_attachment import \
    InternalAttachmentDetails
from org.ict_ok.components.adapter.rpt_pdf import \
     RptPdf as ParentRptPdf
from org.ict_ok.admin_utils.reports.interfaces import IRptPdf


class RptPdf(ParentRptPdf):
    """adapter implementation of Internal Attachment -> PDF Report
    """

    implements(IRptPdf)
    adapts(IInternalAttachment)
    factory = InternalAttachment
    omitFields = InternalAttachmentDetails.omit_viewfields

