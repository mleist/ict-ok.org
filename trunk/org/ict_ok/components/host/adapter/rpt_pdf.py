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
from zope.app import zapi
from zope.interface import implements
from zope.component import adapts
from zope.app.catalog.interfaces import ICatalog

# z3c imports
from z3c.form import field

# reportlab imports
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import Spacer, KeepTogether
from reportlab.platypus.tables import Table, TableStyle

# ict_ok.org imports
from org.ict_ok.components.host.interfaces import IHost
from org.ict_ok.components.supernode.interfaces import IState
from org.ict_ok.components.supernode.adapter.rpt_pdf import \
     RptPdf as ParentRptPdf
from org.ict_ok.admin_utils.reports.interfaces import IRptPdf
from org.ict_ok.admin_utils.reports.rpt_para import RptPara
from org.ict_ok.admin_utils.reports.rpt_style import getRptStyleSheet
from org.ict_ok.admin_utils.compliance.evaluation import getEvaluations


class RptPdf(ParentRptPdf):
    """adapter implementation of latency -> PDF Report
    """

    implements(IRptPdf)
    adapts(IHost)

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
                #return elemList
            if self.context.requirement is not None:
                my_catalog = zapi.getUtility(ICatalog)
                res = my_catalog.searchResults(oid_index=self.context.requirement)
                if len(res) > 0:
                    requirementObj = iter(res).next()
                    reqTitle = requirementObj.ikName
                    reqComment = requirementObj.ikComment
                    elemList.append(RptPara(reqTitle,
                                            doc=self.document))
                    elemList.append(RptPara(reqComment,
                                            doc=self.document))
                    elemList.append(Spacer(0, 4 * mm))
            # Evaluations
            evaluations = getEvaluations(self.context)
            if len(evaluations) > 0:
                styleSheet = getRptStyleSheet()
                style1 = styleSheet['Small']
                style2 = styleSheet['Infobox']
                elemList.append(
                    RptPara('Evaluations: ', style=style2, doc=self.document))
                colWidths = [75 * mm, 20 * mm, 40 * mm]
                data = [[
                    RptPara('<b>Requirement</b>', style=style1, doc=self.document),
                    RptPara('<b>Value</b>', style=style1, doc=self.document),
                    RptPara('<b>Evaluator</b>', style=style1, doc=self.document)
                ]]
                ik_tbl_style = TableStyle([\
                    ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                    ('LEFTPADDING', (0,0), (-1,-1), 2 * mm),
                    ('RIGHTPADDING', (0,0), (-1,-1), 2 * mm),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 2 * mm),
                    ('TOPPADDING', (0,0), (-1,-1), 2 * mm),
                    ('FONTSIZE', (0,0), (-1,-1), 8),
                    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                ])
                pos = 0
                for evaluation in evaluations.values():
                    pos = pos + 1
                    if evaluation.value == 'Pass':
                        ik_tbl_style.add('BACKGROUND', (1,pos), (1,pos), colors.green)
                    elif evaluation.value == 'Fail':
                        ik_tbl_style.add('BACKGROUND', (1,pos), (1,pos), colors.red)
                    else:
                        pass
                    data.append([
                        RptPara(evaluation.requirement.ikName,
                                style=style1,
                                doc=self.document),
                        RptPara(evaluation.value,
                                style=style1, 
                                doc=self.document),
                        RptPara(evaluation.evaluator.title,
                                style=style1, 
                                doc=self.document),
                    ])
                t0 = Table(data,
                           hAlign='RIGHT',
                           style=ik_tbl_style,
                           colWidths=colWidths)
                elemList.append(t0)
                elemList.append(Spacer(0, 4 * mm))
            #for evaluation in evaluations.values():
                #para = RptPara("Eval111",
                               #doc=self.document)
                #elemList.append(para)
            if autoAppend is True:
                #comp = KeepTogether(elemList)
                #self.document.append(comp)
                for elem in elemList:
                    self.document.append(elem)
            else:
                return elemList
        return None

