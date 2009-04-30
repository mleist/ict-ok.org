# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# no_pylint: disable-msg=W0232
#
"""rpt_font module 

font-class for ict-ok.org reporting 
"""

__version__ = "$Id$"

# phython imports
import os

# zope imports
from zope.component import getUtility

# reportlab imports
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.fonts import addMapping

# ict-ok.org imports
from org.ict_ok.admin_utils.reports.interfaces import IAdmUtilReports

def __registerFont__(fontname, afmFilename, pfbFilename):
    justFace = pdfmetrics.EmbeddedType1Face(afmFilename, pfbFilename)
    pdfmetrics.registerTypeFace(justFace)
    justFont = pdfmetrics.Font(fontname, fontname, 'WinAnsiEncoding')
    pdfmetrics.registerFont(justFont)

def registerRptFonts():
    admUtilReports = getUtility(IAdmUtilReports, name='AdmUtilReports')
    if admUtilReports.fontName1 is not None and \
       admUtilReports.afmFile1 is not None and \
       admUtilReports.pfbFile1 is not None:
        __registerFont__(admUtilReports.fontName1,
                         admUtilReports.afmFile1,
                         admUtilReports.pfbFile1)
        # normal
        addMapping(admUtilReports.fontName1, 0, 0, admUtilReports.fontName1)
    if admUtilReports.fontName2 is not None and \
       admUtilReports.afmFile2 is not None and \
       admUtilReports.pfbFile2 is not None:
        __registerFont__(admUtilReports.fontName2,
                         admUtilReports.afmFile2,
                         admUtilReports.pfbFile2)
        # bold
        addMapping(admUtilReports.fontName1, 1, 0, admUtilReports.fontName2)
    if admUtilReports.fontName3 is not None and \
       admUtilReports.afmFile3 is not None and \
       admUtilReports.pfbFile3 is not None:
        __registerFont__(admUtilReports.fontName3,
                         admUtilReports.afmFile3,
                         admUtilReports.pfbFile3)
        # italic
        addMapping(admUtilReports.fontName1, 0, 1, admUtilReports.fontName3)
    if admUtilReports.fontName4 is not None and \
       admUtilReports.afmFile4 is not None and \
       admUtilReports.pfbFile4 is not None:
        __registerFont__(admUtilReports.fontName4,
                         admUtilReports.afmFile4,
                         admUtilReports.pfbFile4)
        # italic and bold
        addMapping(admUtilReports.fontName1, 1, 1, admUtilReports.fontName4)
    if admUtilReports.fontName5 is not None and \
       admUtilReports.afmFile5 is not None and \
       admUtilReports.pfbFile5 is not None:
        __registerFont__(admUtilReports.fontName5,
                         admUtilReports.afmFile5,
                         admUtilReports.pfbFile5)

    #afmFile = os.path.join(folder, '5.afm')
    #pfbFile = os.path.join(folder, '5.pfb')
    
    #justFace = pdfmetrics.EmbeddedType1Face(afmFile, pfbFile)
    #faceName = 'MetaKorrespondenz-Roman' # pulled from AFM file
    #pdfmetrics.registerTypeFace(justFace)
    #justFont = pdfmetrics.Font('MetaKorrespondenz-Roman', faceName, 'WinAnsiEncoding')
    #pdfmetrics.registerFont(justFont)
    
    #afmFile = os.path.join(folder, 'MetaKorrespondenz-Italic.afm')
    #pfbFile = os.path.join(folder, 'MetaKorrespondenz-Italic.pfb')
    #justFace = pdfmetrics.EmbeddedType1Face(afmFile, pfbFile)
    #faceName = 'MetaKorrespondenz-Italic' # pulled from AFM file
    #pdfmetrics.registerTypeFace(justFace)
    #justFont = pdfmetrics.Font('MetaKorrespondenz-Italic', faceName, 'WinAnsiEncoding')
    #pdfmetrics.registerFont(justFont)
    
    #afmFile = os.path.join(folder, 'MetaKorrespondenz-Bold.afm')
    #pfbFile = os.path.join(folder, 'MetaKorrespondenz-Bold.pfb')
    #justFace = pdfmetrics.EmbeddedType1Face(afmFile, pfbFile)
    #faceName = 'MetaKorrespondenz-Bold' # pulled from AFM file
    #pdfmetrics.registerTypeFace(justFace)
    #justFont = pdfmetrics.Font('MetaKorrespondenz-Bold', faceName, 'WinAnsiEncoding')
    #pdfmetrics.registerFont(justFont)

def addMappingRptFonts():
    addMapping('MetaKorrespondenz-Roman', 0, 0, 'MetaKorrespondenz-Roman')    #normal
    addMapping('MetaKorrespondenz-Roman', 0, 1, 'MetaKorrespondenz-Italic')    #italic
    addMapping('MetaKorrespondenz-Roman', 1, 0, 'MetaKorrespondenz-Bold')    #bold
    addMapping('MetaKorrespondenz-Roman', 1, 1, 'MetaKorrespondenz-Bold')    #italic and bold
