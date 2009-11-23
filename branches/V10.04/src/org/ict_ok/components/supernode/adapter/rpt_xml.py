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
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.components.supernode.interfaces import ISupernode
from org.ict_ok.components.superclass.adapter.rpt_xml import \
     RptXML as ParentRptXML
from org.ict_ok.admin_utils.reports.interfaces import IRptXML

logger = logging.getLogger("SupernodeGenSmokePing")


class RptXML(ParentRptXML):
    """adapter implementation of Supernode -> XML Report
    """

    implements(IRptXML)
    adapts(ISupernode)

    attributeList = []
    attributeList.extend(ParentRptXML.attributeList)
    
    def traverse4RptBody(self, level, comments):
        """xml report data of/in object
        
        level: indent-level (int 0..)
        comments: should there comments are in the output?
        """
        if comments:
            self.writeComment(u"%s## Body (%s,%d) - SupernodeRptXMLBody" % \
                              ("\t" * level, self.context.ikName, level))
        its = self.context.items()
        for (dummy_name, oobj) in its:
            if ISuperclass.providedBy(oobj):
                try:
                    adapterRptXML = IRptXML(oobj)
                    if adapterRptXML:
                        adapterRptXML.document = self.document
                        adapterRptXML.traverse4Rpt(level + 1, comments)
                        #self.files2delete.extend(adapterRptPdf.files2delete)
                        del adapterRptXML
                except TypeError, errText:
                    logger.error(u"Problem in adaption: %s (%s)" %\
                                 (errText, oobj.ikName))
