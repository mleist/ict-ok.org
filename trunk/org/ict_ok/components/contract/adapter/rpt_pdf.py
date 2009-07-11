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
"""Adapter implementation for generating pdf reports of Contract"""

__version__ = "$Id: rpt_pdf.py_cog 519 2009-05-12 07:44:37Z markusleist $"

# python imports

# zope imports
from zope.interface import implements
from zope.component import adapts

# z3c imports
from z3c.form import field

# ict_ok.org imports
from org.ict_ok.components.contract.interfaces import IContract
from org.ict_ok.components.contract.contract import Contract
from org.ict_ok.components.contract.browser.contract import \
    ContractDetails
from org.ict_ok.components.adapter.rpt_pdf import \
     RptPdf as ParentRptPdf
from org.ict_ok.admin_utils.reports.interfaces import IRptPdf


class RptPdf(ParentRptPdf):
    """adapter implementation of Contract -> PDF Report
    """

    implements(IRptPdf)
    adapts(IContract)
    factory = Contract
    omitFields = ContractDetails.omit_viewfields

