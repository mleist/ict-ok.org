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
"""Adapter implementation for generating pdf reports of Product"""

__version__ = "$Id: rpt_pdf.py_cog 506 2009-04-30 14:24:56Z markusleist $"

# python imports
import logging

# zope imports
from zope.interface import implements
from zope.component import adapts

# z3c imports
from z3c.form import field

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.components.product.interfaces import IProduct
from org.ict_ok.components.product.product import Product
from org.ict_ok.components.product.browser.product import \
    ProductDetails
from org.ict_ok.components.supernode.adapter.rpt_pdf import \
     RptPdf as ParentRptPdf
from org.ict_ok.admin_utils.reports.interfaces import IRptPdf

logger = logging.getLogger("ProductGenPdf")


class RptPdf(ParentRptPdf):
    """adapter implementation of Product -> PDF Report
    """

    implements(IRptPdf)
    adapts(IProduct)
    factory = Product
    omitFields = ProductDetails.omit_viewfields

    def traverse4RptBody(self, level, comments):
        """pdf report data of/in object
        
        level: indent-level (int 0..)
        comments: should there comments are in the output?
        """
        if comments:
            self.writeComment(u"%s## Body (%s,%d) - Product" % \
                              ("\t" * level, self.context.ikName, level))
        its = self.context.subProducts
        for oobj in its:
            if ISuperclass.providedBy(oobj):
                try:
                    adapterRptPdf = IRptPdf(oobj)
                    if adapterRptPdf:
                        adapterRptPdf.document = self.document
                        adapterRptPdf.traverse4Rpt(level + 1, comments)
                        self.files2delete.extend(adapterRptPdf.files2delete)
                        del adapterRptPdf
                except TypeError, errText:
                    logger.error(u"Problem in adaption: %s (%s)" %\
                                 (errText, oobj.ikName))
