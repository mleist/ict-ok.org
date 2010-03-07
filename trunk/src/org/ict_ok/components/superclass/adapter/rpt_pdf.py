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
from zope.i18n import translate
from zope.i18nmessageid.message import Message
from zope.schema import vocabulary

# reportlab imports
from reportlab.lib.units import mm
from reportlab.platypus import Spacer, KeepTogether
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.colors import white, CMYKColor

# z3c imports
from z3c.form import field

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.components.superclass.browser.superclass import \
    SuperclassDetails
from org.ict_ok.admin_utils.reports.interfaces import IRptPdf
from org.ict_ok.admin_utils.reports.rpt_title import RptTitle
from org.ict_ok.admin_utils.reports.rpt_para import RptPara
from org.ict_ok.admin_utils.compliance.adapter.rpt_pdf_tools import \
     appendEvaluationList
from org.ict_ok.admin_utils.reports.rpt_color import \
    getColor1, getLinkColor, \
    getTabBackgroundColor, getTabBackgroundColorLight
from org.ict_ok.components.superclass.superclass import isOidInCatalog
from org.ict_ok.libs.lib import oid2dcTitle

class RptPdf(object):
    """adapter implementation of Superclass -> PDF Report
    """
    
    implements(IRptPdf)
    adapts(ISuperclass)
    factory = Superclass
    omitFields = ['objectID', '__name__', 'ref', 'history',
                  'dbgLevel', 'ikEventTarget']
    
    attributeList = ['ikName']
    
    def __init__(self, context):
        self.document = None
        self.context = context
        self.request = None
        self.files2delete = []
        self.attributeData = []
        self.ikRevision = __version__

    def writeComment(self, text_arg):
        """will write the text_arg into the configuration file
        """
        print "writeComment('%s')" % text_arg
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

    def getRefTitle(self):
        if self.document and \
            self.document._reporter and \
            self.context in \
                self.document._reporter.allContentObjects:
            return u"<a href='%s' color='%s'>%s</a>" % \
                (self.context.objectID,
                 getLinkColor().hexval(),
                 self.context.ikName)
        else:
            return u"%s" % \
                (self.context.ikName)

    def getReportFields(self):
        """
        """
        return fieldsForFactory(self.factory, self.omitFields)
#    def getReportFields(self):
#        """
#        """
#        from org.ict_ok.components.superclass.browser.superclass import \
#             SuperclassDetails
#        return field.Fields(ISuperclass).omit(\
#            *SuperclassDetails.omit_viewfields)

    def _convertNamePara(self, f_obj):
        if type(f_obj) is unicode or \
           type(f_obj) is str:
            reportFieldsTransl = translate(f_obj,
                                           domain='org.ict_ok',
                                           context=self.request)
        elif type(f_obj) is Message: # already translated
            reportFieldsTransl = f_obj
        else: # f_obj is zope.schema-field
            reportFieldsTransl = translate(f_obj.field.title,
                                           domain='org.ict_ok',
                                           context=self.request)
        rptPara = RptPara(reportFieldsTransl,
                           style=self.document.styles['Normal'],
                           doc=self.document)
        return rptPara

    def _convertValPara(self, f_val):
        if ISuperclass.providedBy(f_val):
            rptAdapter = IRptPdf(f_val)
            rptAdapter.request=self.request
            rptAdapter.document = self.document
            iText = rptAdapter.getRefTitle()
        else:
#            if isOidInCatalog(f_val):
#                iText = translate(oid2dcTitle(f_val),
#                                  domain='org.ict_ok',
#                                  context=self.request)
#            else:
            iText = translate(unicode(f_val),
                              domain='org.ict_ok',
                              context=self.request)
        rptPara = RptPara(iText,
                           style=self.document.styles['Normal'],
                           doc=self.document)
        return rptPara

    def _getVocabValue(self, vocabName=None, token=None):
        vocabReg = vocabulary.getVocabularyRegistry()
        if vocabReg is not None:
            vocab = vocabReg.get(self.request, vocabName)
            if vocab is not None:
                try:
                    vocabTerm = vocab.getTerm(token)
                    if vocabTerm:
                        return vocabTerm.title
                except LookupError:
                    return None

    def prependAttributeTable(self):
        return []

    def makeAttributeTable(self):
        data = []
        fields = self.getReportFields()
        for f_name, f_obj in fields.items():
            f_val = getattr(self.context, f_name)
            namePara = self._convertNamePara(f_obj)
            if f_val is not None:
                if f_name in ['user', 'productionState']:
                    token = self._getVocabValue(f_obj.field.vocabularyName,
                                                f_val)
                    valPara = self._convertValPara(token)
                    data.append([namePara, valPara])                    
                elif type(f_val) is str or \
                   type(f_val) is unicode:
                    valPara = self._convertValPara(f_val)
                    data.append([namePara, valPara])
                elif ISuperclass.providedBy(f_val):
                    valPara = self._convertValPara(f_val)
                    data.append([namePara, valPara])
                else:
                    if type(f_val) is list:
                        valParas = []
                        for i in f_val:
                            valParas.append(self._convertValPara(i))
                        if len(valParas) >= 1:
                            data.append([namePara, valParas])
                    else:
                        valPara = self._convertValPara(f_val)
                        data.append([namePara, valPara])
        return data

    def appendAttributeTable(self):
        return []

    def getAttributeTable(self):
        """
        """
        rowColor = getTabBackgroundColor()
        rowColorLight = getTabBackgroundColorLight()
        ik_tbl_style = TableStyle([\
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('ROWBACKGROUNDS',(0,0),(-1,-1),[rowColorLight, rowColor]),
        ])        
        colWidths = [50 * mm, 85 * mm]
        data = []
        data.extend(self.prependAttributeTable())
        data.extend(self.makeAttributeTable())
        data.extend(self.appendAttributeTable())
        if len(data) > 0:
            t0 = Table(data,
                       hAlign = 'RIGHT',
                       style=ik_tbl_style,
                       colWidths=colWidths)
        else:
            t0 = None
        return t0

#-----------------------------------
#        try:
#            it = iter(obj)
#            for i in it:
#                adapterRptPdf = IRptPdf(i)
#                if adapterRptPdf:
#                    adapterRptPdf.request=self.request
#                    adapterRptPdf.document = self.document
#                    adapterRptPdf.traverse4Rpt(1, False)
#                    self.files2delete.extend(adapterRptPdf.files2delete)
#                    del adapterRptPdf
#        except TypeError:
#            adapterRptPdf = IRptPdf(obj)
#            if adapterRptPdf:
#                adapterRptPdf.request=self.request
#                adapterRptPdf.document = self.document
#                adapterRptPdf.traverse4Rpt(1, False)
#                self.files2delete.extend(adapterRptPdf.files2delete)
#                del adapterRptPdf
#----------------------------------


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
                             doc=self.document,
                             context=self.context)
#            elemList = [title.genElements()]
            attrTable = self.getAttributeTable()
            if attrTable:
                elemList = [title.genElements(),
                            self.getAttributeTable(),
                            Spacer(0, 4 * mm)]
            else:
                elemList = [title.genElements(),
                            Spacer(0, 4 * mm)]
            elemList.extend(\
                appendEvaluationList(self.context, self.document))
            if autoAppend is True:
                comp = KeepTogether(elemList)
                self.document.append(comp)
                #for elem in elemList:
                    #self.document.append(elem)
            else:
                return elemList
        return None
    
            #elemList.extend(\
                #appendEvaluationList(self.context, self.document))

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
            if self.document is not None and \
                self.document._reporter is not None:
                self.document._reporter.alreadyReported[self.context.objectID] = self
