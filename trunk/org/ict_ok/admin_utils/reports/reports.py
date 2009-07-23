# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0702,W0221
#
"""implementation of a "Object-Message-Queue-Utility" 
"""

__version__ = "$Id$"

# python imports
import os
import logging

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

# ict_ok.org imports
from org.ict_ok.admin_utils.reports.interfaces import IAdmUtilReports, \
    IRptPdf, IBaseReporter
from org.ict_ok.components.supernode.interfaces import ISupernode
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.admin_utils.reports.rpt_document import RptDocument
from org.ict_ok.admin_utils.reports.rpt_para import RptPara
from org.ict_ok.admin_utils.reports.rpt_title import RptTitle

logger = logging.getLogger("AdmUtilReports")


class AdmUtilReports(Supernode):
    """Implementation of local Reports-Utility"""

    implements(IAdmUtilReports)
    
    color1 = FieldProperty(IAdmUtilReports['color1'])
    logoFile1 = FieldProperty(IAdmUtilReports['logoFile1'])
    fontName1 = FieldProperty(IAdmUtilReports['fontName1'])
    fontName2 = FieldProperty(IAdmUtilReports['fontName2'])
    fontName3 = FieldProperty(IAdmUtilReports['fontName3'])
    fontName4 = FieldProperty(IAdmUtilReports['fontName4'])
    fontName5 = FieldProperty(IAdmUtilReports['fontName5'])
    afmFile1 = FieldProperty(IAdmUtilReports['afmFile1'])
    pfbFile1 = FieldProperty(IAdmUtilReports['pfbFile1'])
    afmFile2 = FieldProperty(IAdmUtilReports['afmFile2'])
    pfbFile2 = FieldProperty(IAdmUtilReports['pfbFile2'])
    afmFile3 = FieldProperty(IAdmUtilReports['afmFile3'])
    pfbFile3 = FieldProperty(IAdmUtilReports['pfbFile3'])
    afmFile4 = FieldProperty(IAdmUtilReports['afmFile4'])
    pfbFile4 = FieldProperty(IAdmUtilReports['pfbFile4'])
    afmFile5 = FieldProperty(IAdmUtilReports['afmFile5'])
    pfbFile5 = FieldProperty(IAdmUtilReports['pfbFile5'])

    def __init__(self):
        Supernode.__init__(self)
        self.ikRevision = __version__

    def generateAllPdf(self, absFilename, authorStr, versionStr):
        """
        will generate a complete pdf report
        """
        files2delete = []
        document = RptDocument(absFilename)
        #document.setVolumeNo("1")
        document.setAuthorName(authorStr)
        document.setVersionStr(versionStr)
        its = zapi.getRoot(self).items()
        for (dummy_name, oobj) in its:
            if ISupernode.providedBy(oobj):
                try:
                    adapterRptPdf = IRptPdf(oobj)
                    if adapterRptPdf:
                        adapterRptPdf.document = document
                        adapterRptPdf.traverse4Rpt(1, False)
                        files2delete.extend(adapterRptPdf.files2delete)
                        del adapterRptPdf
                except TypeError, errText:
                    logger.error(u"Problem in adaption of pdf report: %s" %\
                                 (errText))
        document.buildPdf()
        for i_filename in files2delete:
            try:
                os.remove(i_filename)
            except OSError:
                pass

class BaseReporter(object):
    """
    """
    implements(IBaseReporter)

#    firstLevelContent = FieldProperty(IBaseReporter['firstLevelContent'])
    allContentObjects = FieldProperty(IBaseReporter['allContentObjects'])
    alreadyReported = FieldProperty(IBaseReporter['alreadyReported'])
    
    def __init__(self):
#        self.firstLevelContent = []
        self.allContentObjects = set([])
        self.alreadyReported = {}
    
class SimpleReporter(BaseReporter):
    """
    """

class PDFReporter(SimpleReporter):
    """
    """
    def __init__(self, absFilename, request=None):
        self.files2delete = []
        self.document = RptDocument(absFilename)
        self.document.setReporter(self)
        self.request = request
        SimpleReporter.__init__(self)

        
    def setVolumeNo(self, volumeStr):
        self.document.setVolumeNo(volumeStr)

    def setAuthorName(self, authorStr):
        self.document.setAuthorName(authorStr)
        
    def setVersionStr(self, versionStr):
        self.document.setVersionStr(versionStr)
    
    def cleanup(self):
        for i_filename in self.files2delete:
            try:
                os.remove(i_filename)
            except OSError:
                pass
            
    def extendAllContentObjects(self, objList):
        for obj in objList:
            self.allContentObjects.add(obj)

#    def fill(self):
#        self.append(self.firstLevelContent)

    def appendTitle1(self, title):
        title = RptTitle(title, doc=self.document, intype='Heading1')
        self.document.append(title.genElements())
        
    def appendTitle2(self, title):
        title = RptTitle(title, doc=self.document, intype='Heading2')
        self.document.append(title.genElements())
        
    def append(self, obj):
        if type(obj) is list:
            for i in obj:
                #self.firstLevelContent.append(i)
                adapterRptPdf = IRptPdf(i)
                if adapterRptPdf:
                    adapterRptPdf.request=self.request
                    adapterRptPdf.document = self.document
                    adapterRptPdf.traverse4Rpt(2, False)
                    self.files2delete.extend(adapterRptPdf.files2delete)
                    del adapterRptPdf
        else:
            adapterRptPdf = IRptPdf(obj)
            if adapterRptPdf:
                adapterRptPdf.request=self.request
                adapterRptPdf.document = self.document
                adapterRptPdf.traverse4Rpt(2, False)
                self.files2delete.extend(adapterRptPdf.files2delete)
                del adapterRptPdf

    def buildPdf(self):
        self.document.buildPdf()
