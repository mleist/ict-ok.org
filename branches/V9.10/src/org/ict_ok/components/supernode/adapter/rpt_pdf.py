# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611
#
"""Configuration adapter for smokeping-config files
"""

__version__ = "$Id$"

# python imports
import logging

# zope imports
from zope.interface import implements
from zope.component import adapts

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import ISupernode
from org.ict_ok.components.superclass.adapter.rpt_pdf import \
     RptPdf as ParentRptPdf
from org.ict_ok.admin_utils.reports.interfaces import IRptPdf

logger = logging.getLogger("SupernodeGenSmokePing")


class RptPdf(ParentRptPdf):
    """adapter implementation of Supernode -> PDF Report
    """

    implements(IRptPdf)
    adapts(ISupernode)
    factory = None
    omitFields = ParentRptPdf.omitFields + []

    attributeList = []
    attributeList.extend(ParentRptPdf.attributeList)
    
    def traverse4RptBody(self, level, comments):
        """pdf report data of/in object
        
        level: indent-level (int 0..)
        comments: should there comments are in the output?
        """
        if comments:
            self.writeComment(u"%s## Body (%s,%d) - SupernodeRptPdfBody" % \
                              ("\t" * level, self.context.ikName, level))
        its = self.context.items()
        for (dummy_name, oobj) in its:
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
