# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0142
#
"""Adapter implementation for generating pdf
"""


__version__ = "$Id$"

# zope imports
from zope.interface import implements
from zope.component import adapts

# reportlab imports
from reportlab.lib.units import mm
from reportlab.platypus import Spacer, KeepTogether

# ict_ok.org imports
from org.ict_ok.admin_utils.compliance.interfaces import IRequirement
from org.ict_ok.components.supernode.adapter.rpt_pdf import \
     RptPdf as ParentRptPdf
from org.ict_ok.admin_utils.reports.interfaces import IRptPdf
from org.ict_ok.admin_utils.reports.rpt_title import RptTitle
from org.ict_ok.admin_utils.reports.rpt_para import RptPara


class RptRequirementPdf(ParentRptPdf):
    """adapter implementation of latency -> PDF Report
    """

    implements(IRptPdf)
    adapts(IRequirement)

    #def getReportFields(self):
        #"""
        #"""
        #from org.ict_ok.admin_utils.compliance.browser.compliance import \
             #AdmUtilComplianceDetails
        #return field.Fields(IRequirement).omit(\
            #*AdmUtilComplianceDetails.omit_viewfields)
    def traverse4RptPre(self, level, comments, autoAppend=True):
        """pdf report object preamble
        
        level: indent-level (int 0..)
        comments: should there comments are in the output?
        """
        if comments:
            self.writeComment(u"%s## Pre (%s,%d) - SuperclassRptPdfPre" % \
                              ("\t" * level, self.context.ikName, level))
        if self.document is not None:
            className = self.context.myFactory.split('.')[-1]
            if className == 'Requirement':
                titleStr = u"Req.: %s" % \
                         (self.context.ikName)
            else:
                titleStr = u"%s: %s" % \
                         (className,
                          self.context.ikName)
            title = RptTitle(titleStr,
                             intype="Heading%d" % level,
                             doc=self.document)
            stringLines = self.context.ikComment.split('\n')
            newLines = []
            newLine = u""
            for line in stringLines:
                nline = line.strip()
                if len(nline) == 0:
                    if len(newLine):
                        newLines.append(newLine)
                    newLine = u""
                else:
                    newLine += u' %s ' % nline
            if len(newLine):
                newLines.append(newLine)
            parasString = ' '.join(stringLines)
            elemList = [title.genElements()]
            #elemList = [title.genElements(),
                        #RptPara(self.context.ikComment, doc=self.document),
                        #Spacer(0, 4 * mm)
                        #]
            for paraLine in newLines:
                para = RptPara(paraLine, doc=self.document)
                elemList.append(para)
            elemList.append(Spacer(0, 4 * mm))
            if autoAppend is True:
                comp = KeepTogether(elemList)
                self.document.append(comp)
            else:
                return elemList
        return None

