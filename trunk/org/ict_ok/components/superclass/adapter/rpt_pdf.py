# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0704,W0142
#
"""Configuration adapter for smokeping-config files
"""

__version__ = "$Id$"

# python imports
import os

# zope imports
from zope.interface import implements
from zope.component import adapts

# reportlab imports
from reportlab.lib.units import mm
from reportlab.platypus import Spacer, KeepTogether
from reportlab.platypus.tables import Table, TableStyle

# z3c imports
from z3c.form import field

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.components.component import IComponent
from org.ict_ok.admin_utils.reports.interfaces import IRptPdf
from org.ict_ok.admin_utils.reports.rpt_title import RptTitle
from org.ict_ok.admin_utils.reports.rpt_para import RptPara


class RptPdf(object):
    """adapter implementation of Superclass -> PDF Report
    """
    
    implements(IRptPdf)
    adapts(ISuperclass)
    
    attributeList = ['ikName']
    
    def __init__(self, context):
        self.document = None
        self.context = context
        self.files2delete = []
        self.attributeData = []
        self.ikRevision = __version__

    def writeComment(self, text_arg):
        """will write the text_arg into the configuration file
        """
        if self.document is not None:
            rptPara = RptPara(text_arg, doc=self.document)
            self.document.append(rptPara)

    def appendFile2Delete(self, absFilename):
        """will delete this file AFTER rendering pdf
        """
        if os.path.exists(absFilename):
            self.files2delete.append(absFilename)

    def cleanupFiles(self):
        """will delete all used files AFTER rendering pdf
        """
        for i_filename in self.files2delete:
            try:
                os.remove(i_filename)
            except OSError:
                pass

    def getReportFields(self):
        """
        """
        from org.ict_ok.components.superclass.browser.superclass import \
             SuperclassDetails
        return field.Fields(ISuperclass).omit(\
            *SuperclassDetails.omit_viewfields)

    def getAttributeTable(self):
        """
        """
        ik_tbl_style = TableStyle([\
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ])        
        colWidths = [50 * mm, 85 * mm]
        data = []
        fields = self.getReportFields()
        for f_name, f_obj in fields.items():
            f_val = getattr(self.context, f_name)
            if f_val is not None:
                rptPara = RptPara(unicode(f_val), doc=self.document)
                data.append([f_obj.field.title, rptPara])
        if len(data) > 0:
            t0 = Table(data,
                       hAlign = 'RIGHT',
                       style=ik_tbl_style,
                       colWidths=colWidths)
        else:
            t0 = None
        return t0

    def traverse4RptPre(self, level, comments, autoAppend=True):
        """pdf report object preamble
        
        level: indent-level (int 0..)
        comments: should there comments are in the output?
        """
        if comments:
            self.writeComment(u"%s## Pre (%s,%d) - SuperclassRptPdfPre" % \
                              ("\t" * level, self.context.ikName, level))
        if self.document is not None:
            titleStr = u"%s: %s" % \
                     (self.context.myFactory.split('.')[-1],
                      self.context.ikName)
            title = RptTitle(titleStr,
                             intype="Heading%d" % level,
                             doc=self.document)
            elemList = [title.genElements(),
                        self.getAttributeTable(),
                        Spacer(0, 4 * mm)]
            if autoAppend is True:
                comp = KeepTogether(elemList)
                self.document.append(comp)
                #for elem in elemList:
                    #self.document.append(elem)
            else:
                return elemList
        return None

    def traverse4RptPost(self, level, comments):
        """pdf report object postamble
        
        level: indent-level (int 0..)
        comments: should there comments are in the output?
        """
        if comments:
            self.writeComment(u"%s## Post (%s,%d) - SuperclassRptPdfPost" % \
                              ("\t" * level, self.context.ikName, level))

    def traverse4RptBody(self, level, comments):
        """pdf report data of/in object
        
        level: indent-level (int 0..)
        comments: should there comments are in the output?
        """
        if comments:
            self.writeComment(u"%s## Body (%s,%d) - SuperclassRptPdfBody" % \
                              ("\t" * level, self.context.ikName, level))

    def traverse4Rpt(self, level, comments):
        """object pdf report
        
        level: indent-level (int 0..)
        comments: should there comments are in the output?
        """
        if ISuperclass.providedBy(self.context):
            self.traverse4RptPre(level, comments)
            self.traverse4RptBody(level, comments)
            self.traverse4RptPost(level, comments)
