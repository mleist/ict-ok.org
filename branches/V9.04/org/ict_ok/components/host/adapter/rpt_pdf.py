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
"""Adapter implementation for generating graphviz-dot configuration
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.component import adapts

# z3c imports
from z3c.form import field

# reportlab imports
from reportlab.lib.units import mm
from reportlab.platypus import Spacer

# ict_ok.org imports
from org.ict_ok.components.host.interfaces import IHost
from org.ict_ok.components.supernode.interfaces import IState
from org.ict_ok.components.supernode.adapter.rpt_pdf import \
     RptPdf as ParentRptPdf
from org.ict_ok.admin_utils.reports.interfaces import IRptPdf
from org.ict_ok.admin_utils.reports.rpt_para import RptPara


class RptPdf(ParentRptPdf):
    """adapter implementation of latency -> PDF Report
    """

    implements(IRptPdf)
    adapts(IHost)
    factory = None
    omitFields = None

    def getReportFields(self):
        """
        """
        from org.ict_ok.components.host.browser.host import HostDetails
        omitField = [
            'snmpVersion',
            'snmpPort',
            'snmpReadCommunity',
            'snmpWriteCommunity',
            'url',
            'url_type',
            'url_authname',
            'url_authpasswd',
            'console',
            'genNagios',
            'requirement',
            'hostGroups',
        ]
        omitField.extend(HostDetails.omit_viewfields)
        return field.Fields(IHost).omit(*omitField)

    def traverse4RptPre(self, level, comments, autoAppend=True):
        """pdf report object preamble
        
        level: indent-level (int 0..)
        comments: should there comments are in the output?
        """
        if self.document is not None:
            elemList = ParentRptPdf.traverse4RptPre(\
                self, level, comments, autoAppend)
            if elemList is None:
                elemList = []
            try:
                stateDict = IState(self.context).getStateDict()
                if stateDict['overview'] == 'error':
                    myStyle = self.document.styles['ErrorBox']
                elif stateDict['overview'] == 'warn':
                    myStyle = self.document.styles['WarnBox']
                else:
                    myStyle = None
                if myStyle is not None:
                    para = RptPara(stateDict['warnings'][0],
                                   style=myStyle, doc=self.document)
                    elemList.extend([Spacer(0, 4 * mm),
                                     para,
                                     Spacer(0, 4 * mm)])
            except TypeError:
                pass
            if autoAppend is True:
                #comp = KeepTogether(elemList)
                #self.document.append(comp)
                for elem in elemList:
                    self.document.append(elem)
            else:
                return elemList
        return None

