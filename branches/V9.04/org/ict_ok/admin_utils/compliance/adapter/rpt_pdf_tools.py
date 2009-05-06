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

# python imports

# zope imports
from zope.app import zapi
from zope.app.catalog.interfaces import ICatalog

# reportlab imports
from reportlab.lib.units import mm
from reportlab.platypus import Spacer
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib import colors

# ict_ok.org imports
from org.ict_ok.admin_utils.reports.rpt_para import RptPara
from org.ict_ok.admin_utils.reports.rpt_style import getRptStyleSheet
from org.ict_ok.admin_utils.compliance.evaluation import \
    getEvaluationsDone, getEvaluationsTodo
from org.ict_ok.admin_utils.reports.rpt_color import \
    getColor1, getLinkColor, \
    getTabBackgroundColor, getTabBackgroundColorLight


def appendEvaluationList(obj, document):
    elemList = []
    if hasattr(obj, 'requirement') \
       and obj.requirement is not None:
        my_catalog = zapi.getUtility(ICatalog)
        res = my_catalog.searchResults(oid_index=obj.requirement)
        if len(res) > 0:
            requirementObj = iter(res).next()
            reqTitle = requirementObj.ikName
            reqComment = requirementObj.ikComment
            elemList.append(RptPara(reqTitle,
                                    doc=document))
            elemList.append(RptPara(reqComment,
                                    doc=document))
            elemList.append(Spacer(0, 4 * mm))
    # Evaluations Done
    evaluations = getEvaluationsDone(obj)
    if len(evaluations) > 0:
        styleSheet = getRptStyleSheet()
        style1 = styleSheet['Small']
        style2 = styleSheet['Infobox']
        elemList.append(
            RptPara('Evaluations Done: ', style=style2, doc=document))
        colWidths = [15 * mm, 60 * mm, 20 * mm, 40 * mm]
        data = [[
            RptPara('<b>Pos</b>', style=style1, doc=document),
            RptPara('<b>Requirement</b>', style=style1, doc=document),
            RptPara('<b>Value</b>', style=style1, doc=document),
            RptPara('<b>Evaluator</b>', style=style1, doc=document)
        ]]
        rowColor = getTabBackgroundColor()
        rowColorLight = getTabBackgroundColorLight()
        ik_tbl_style = TableStyle([\
            ('BACKGROUND', (0, 0), (-1, 0), rowColor),
            ('LEFTPADDING', (0, 0), (-1, -1), 1 * mm),
            ('RIGHTPADDING', (0, 0), (-1, -1), 1 * mm),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1 * mm),
            ('TOPPADDING', (0, 0), (-1, -1), 2 * mm),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ROWBACKGROUNDS',(0,0),(-1,-1),[rowColor, rowColorLight]),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ])
        pos = 0
        for evaluation in evaluations.values():
            pos = pos + 1
            if evaluation.value == 'Pass':
                ik_tbl_style.add('BACKGROUND', (2, pos), (2, pos), colors.green)
            elif evaluation.value == 'Fail':
                ik_tbl_style.add('BACKGROUND', (2, pos), (2, pos), colors.red)
            else:
                pass
            if len(evaluation.requirement) == 0:
                data.append([
                    RptPara(evaluation.requirement.getIndexString(),
                            style=style1,
                            doc=document),
                    RptPara(evaluation.requirement.ikName,
                            style=style1,
                            doc=document),
                    RptPara(evaluation.value,
                            style=style1, 
                            doc=document),
                    RptPara(evaluation.evaluator.title,
                            style=style1, 
                            doc=document),
                ])
        t0 = Table(data,
                   hAlign='RIGHT',
                   style=ik_tbl_style,
                   colWidths=colWidths)
        elemList.append(t0)
        elemList.append(Spacer(0, 3 * mm))
    # Evaluations ToDo
    evaluations = getEvaluationsTodo(obj)
    if len(evaluations) > 0:
        styleSheet = getRptStyleSheet()
        style1 = styleSheet['Small']
        style2 = styleSheet['Infobox']
        elemList.append(
            RptPara('Evaluations ToDo: ', style=style2, doc=document))
        #colWidths = [75 * mm, 20 * mm, 40 * mm]
        colWidths = [15 * mm, 120 * mm]
        data = [[
            RptPara('<b>Pos</b>', style=style1, doc=document),
            RptPara('<b>Requirement</b>', style=style1, doc=document),
            #RptPara('<b>Value</b>', style=style1, doc=document),
            #RptPara('<b>Evaluator</b>', style=style1, doc=document)
        ]]
        rowColor = getTabBackgroundColor()
        rowColorLight = getTabBackgroundColorLight()
        ik_tbl_style = TableStyle([\
            ('BACKGROUND', (0, 0), (-1, 0), rowColor),
            ('LEFTPADDING', (0, 0), (-1, -1), 1 * mm),
            ('RIGHTPADDING', (0, 0), (-1, -1), 1 * mm),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1 * mm),
            ('TOPPADDING', (0, 0), (-1, -1), 2 * mm),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ROWBACKGROUNDS',(0,0),(-1,-1),[rowColor, rowColorLight]),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ])
        #pos = 0
        for evaluation in evaluations:
#            import pdb
#            pdb.set_trace()
#            pos = pos + 1
#            if evaluation.value == 'Pass':
#                ik_tbl_style.add('BACKGROUND', (1, pos), (1, pos), colors.green)
#            elif evaluation.value == 'Fail':
#                ik_tbl_style.add('BACKGROUND', (1, pos), (1, pos), colors.red)
#            else:
#                pass
            if len(evaluation.keys()) == 0:
                data.append([
                    RptPara(evaluation.getIndexString(),
                            style=style1,
                            doc=document),
                    RptPara(evaluation.ikName,
                            style=style1,
                            doc=document),
#                RptPara(evaluation.value,
#                        style=style1, 
#                        doc=document),
#                RptPara(evaluation.evaluator.title,
#                        style=style1, 
#                        doc=document),
            ])
        t0 = Table(data,
                   hAlign='RIGHT',
                   style=ik_tbl_style,
                   colWidths=colWidths)
        elemList.append(t0)
        elemList.append(Spacer(0, 3 * mm))
    return elemList
