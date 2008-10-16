# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: interfaces.py 350 2008-10-12 09:18:43Z markusleist $
#
# no_pylint: disable-msg=W0232
#
"""rpt_stype module 

style-class for ict-ok.org reporting 
"""

__version__ = "$Id: $"

# phython imports

# zope imports
from zope.component import getUtility

# reportlab imports
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import \
     TA_CENTER, ParagraphStyle, StyleSheet1

# ict-ok.org imports
from org.ict_ok.admin_utils.reports.rpt_color import colors, CMYK_RPT1
from org.ict_ok.admin_utils.reports.interfaces import IAdmUtilReports

#rptNormalStyle = ParagraphStyle(name='Normal',
                                #fontName='Helvetica',
                                #fontSize=10,
                                #leading=12)

#rptHeading1Style = ParagraphStyle(name='Heading1',
                                  #keepWithNext = 1,
                                  #fontName = 'Helvetica-Bold',
                                  #fontSize=18,
                                  #leading=22,
                                  #spaceAfter=6)

def getRptStyleSheet():
    """Returns a stylesheet object"""
    
    admUtilReports = getUtility(IAdmUtilReports)

    if admUtilReports.fontName1 is None:
        locFontName1 = 'Helvetica'
    else:
        locFontName1 = admUtilReports.fontName1
    if admUtilReports.fontName2 is None:
        locFontName2 = 'Helvetica-Bold'
    else:
        locFontName2 = admUtilReports.fontName2
    if admUtilReports.fontName1 is None:
        locFontName3 = 'Helvetica-Oblique'
    else:
        locFontName3 = admUtilReports.fontName3
    if admUtilReports.fontName1 is None:
        locFontName4 = 'Helvetica-BoldOblique'
    else:
        locFontName4 = admUtilReports.fontName4
    if admUtilReports.fontName1 is None:
        locFontName5 = 'Courier'
    else:
        locFontName5 = admUtilReports.fontName5

    stylesheet = StyleSheet1()
    stylesheet.add(ParagraphStyle(name='Normal',
                                  fontName=locFontName1,
                                  fontSize=10,
                                  leading=12)
                   )
    stylesheet.add(ParagraphStyle(name='Para',
                                  fontName=locFontName1,
                                  fontSize=10,
                                  leftIndent = 30*mm,
                                  leading=12)
                   )
    stylesheet.add(ParagraphStyle(name='Infobox',
                                  parent=stylesheet['Para'],
                                  backColor = colors.lightgrey)
                   )
    stylesheet.add(ParagraphStyle(name='Normal_R',
                                  fontName=locFontName1,
                                  fontSize=10,
                                  alignment=2,
                                  leading=12)
                   )
    stylesheet.add(ParagraphStyle(name='BodyText',
                                  parent=stylesheet['Normal'],
                                  spaceBefore=6)
                   )
    stylesheet.add(ParagraphStyle(name='Italic',
                                  parent=stylesheet['BodyText'],
                                  fontName = locFontName3)
                   )
    stylesheet.add(ParagraphStyle(name='Heading1',
                                  parent=stylesheet['Normal'],
                                  #backColor = colors.cyan,
                                  keepWithNext = 1,
                                  fontName = locFontName2,
                                  fontSize=18,
                                  leading=22,
                                  spaceBefore = 1*cm,
                                  spaceAfter=12),
                   alias='h1')
    stylesheet.add(ParagraphStyle(name='Heading1r',
                                  parent=stylesheet['Heading1'],
                                  textColor = CMYK_RPT1,
                                  alignment=2)
                              )
    stylesheet.add(ParagraphStyle(name='Heading2',
                                  parent=stylesheet['Normal'],
                                  #backColor = colors.green,
                                  keepWithNext = 1,
                                  fontName = locFontName2,
                                  fontSize=14,
                                  leading=18,
                                  spaceBefore=20,
                                  spaceAfter=12),
                   alias='h2')
    stylesheet.add(ParagraphStyle(name='Heading2r',
                                  parent=stylesheet['Heading2'],
                                  textColor = CMYK_RPT1,
                                  alignment=2)
                              )
    stylesheet.add(ParagraphStyle(name='Heading3',
                                  parent=stylesheet['Normal'],
                                  keepWithNext = 1,
                                  fontName = locFontName2,
                                  fontSize=12,
                                  leading=14,
                                  spaceBefore=20,
                                  spaceAfter=12),
                   alias='h3')
    stylesheet.add(ParagraphStyle(name='Heading3r',
                                  parent=stylesheet['Heading3'],
                                  textColor = CMYK_RPT1,
                                  alignment=2)
                              )
    stylesheet.add(ParagraphStyle(name='Heading4',
                                  parent=stylesheet['Normal'],
                                  keepWithNext = 1,
                                  fontName = locFontName2,
                                  fontSize=10,
                                  leading=14,
                                  spaceBefore=2*mm,
                                  spaceAfter=12),
                   alias='h4')
    stylesheet.add(ParagraphStyle(name='Heading4r',
                                  parent=stylesheet['Heading4'],
                                  textColor = CMYK_RPT1,
                                  alignment=2)
                              )
    stylesheet.add(ParagraphStyle(name='Title',
                                  parent=stylesheet['Normal'],
                                  fontName = locFontName2,
                                  fontSize=18,
                                  leading=22,
                                  alignment=TA_CENTER,
                                  spaceAfter=6),
                   alias='title')
    stylesheet.add(ParagraphStyle(name='Bullet',
                                  parent=stylesheet['Normal'],
                                  firstLineIndent=0,
                                  spaceBefore=3),
                   alias='bu')
    stylesheet.add(ParagraphStyle(name='Definition',
                                  parent=stylesheet['Normal'],
                                  firstLineIndent=0,
                                  leftIndent=36,
                                  bulletIndent=0,
                                  spaceBefore=6,
                                  bulletFontName=locFontName3),
                   alias='df')
    stylesheet.add(ParagraphStyle(name='Code',
                                  parent=stylesheet['Normal'],
                                  fontName=locFontName5,
                                  fontSize=8,
                                  leading=8.8,
                                  firstLineIndent=0,
                                  leftIndent=36))
    return stylesheet
