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
import os

# zope imports
from zope.interface import implements
from zope.component import adapts

# reportlab imports
from reportlab.lib.units import mm, cm
from reportlab.platypus import Image, Spacer
from reportlab.platypus.tables import Table, TableStyle

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

    def getAttributeTable(self):
        """
        """
        print "88888"
        #ik_tbl_style = TableStyle([\
            ##('LEFTPADDING', (0,0), (-1,-1), 0),
            ##('RIGHTPADDING', (0,0), (-1,-1), 0),
            ##('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ##('TOPPADDING', (0,0), (-1,-1), 0),
            #('ALIGN', (0,0), (-1,-1), 'LEFT'),
        #])        
        #colWidths = [65 * mm, None]
        #import pdb
        #pdb.set_trace()
        data = []
        from zope.proxy import removeAllProxies
        from zope.component import adaptedBy
        from zope.schema import Field
        from zope.schema.interfaces import IField
        from zope.interface import providedBy
        from zope.schema import getFieldsInOrder
        print "self.__class__: ", self.__class__
        i2s=adaptedBy(self.__class__)
        print "i2s: ", i2s
        for i1 in i2s:
            if i1.isOrExtends(ISuperclass):
                fields = getFieldsInOrder(i1)
                for f_name, f_obj in fields:
                    f_val = getattr(self.context, f_name)
                    if f_val is not None:
                        print "EEE: (%s) -> (%s)" % (f_obj.title, f_val)
                        data.append([f_obj.title, f_val])
                    #import pdb
                    #pdb.set_trace()
                #nads = i1.namesAndDescriptions()
                #for name, obj in nads:
                    #print "UUUUUUUU: ", (name, obj)
                    #if providedBy(obj).isOrExtends(IField):
                        #print "%s /-> %s " % (name, getattr(self.context, name))

        if self.context.ikName is not None:
            data.append([u'Name', self.context.ikName])
        t0 = Table(data)
        #,
                   #style=ik_tbl_style,
                   #colWidths=colWidths)
        return t0
        
    def traverse4RptPre(self, level, comments):
        """pdf report object preamble
        
        level: indent-level (int 0..)
        comments: should there comments are in the output?
        """
        if comments:
            self.writeComment(u"%s## Pre (%s,%d) - SuperclassRptPdfPre" % \
                              ("\t" * level, self.context.ikName, level))
        if self.document is not None:
            title = RptTitle(self.context.ikName,
                             intype="Heading%d" % level,
                             doc=self.document)
            self.document.append(title.genElements())
            self.document.append(self.getAttributeTable())

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
        if IComponent.providedBy(self.context):
            self.traverse4RptPre(level, comments)
            self.traverse4RptBody(level, comments)
            self.traverse4RptPost(level, comments)
