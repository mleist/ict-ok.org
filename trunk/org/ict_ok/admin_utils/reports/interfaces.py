# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0213,E0211,W0232,W0622
#
"""Interface to pdf report generator"""

__version__ = "$Id$"

# python imports
import os

# zope imports
from zope.interface import Interface
from zope.schema import TextLine
from zope.interface import invariant, Invalid
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import ISupernode

_ = MessageFactory('org.ict_ok')


class IAdmUtilReports(ISupernode):
    """A configuration utility."""

    logoFile1 = TextLine(
        title = _("logo1 file path"),
        description = _("Path to logo file (top/left))."),
        readonly = False,
        required = False)

    fontName1 = TextLine(
        title = _("font 1"),
        description = _("normal font"),
        default = u"Helvetica",
        required = True)

    fontName2 = TextLine(
        title = _("font 2"),
        description = _("e.g. heading font"),
        default = u"Helvetica-Bold",
        required = True)

    fontName3 = TextLine(
        title = _("font 3"),
        description = _("e.g. infobox font"),
        default = u"Helvetica-Oblique",
        required = True)

    fontName4 = TextLine(
        title = _("font 4"),
        description = _("e.g. special infobox font"),
        default = u"Helvetica-BoldOblique",
        required = True)

    fontName5 = TextLine(
        title = _("font 5 (code)"),
        description = _("special sourcecode font"),
        default = u"Courier",
        required = True)

    afmFile1 = TextLine(
        title = _("font1 afm path"),
        description = _("Path to afm file."),
        readonly = False,
        required = False)

    pfbFile1 = TextLine(
        title = _("font1 pfb path"),
        description = _("Path to pfb file."),
        readonly = False,
        required = False)

    afmFile2 = TextLine(
        title = _("font2 afm path"),
        description = _("Path to afm file."),
        readonly = False,
        required = False)

    pfbFile2 = TextLine(
        title = _("font2 pfb path"),
        description = _("Path to pfb file."),
        readonly = False,
        required = False)

    afmFile3 = TextLine(
        title = _("font3 afm path"),
        description = _("Path to afm file."),
        readonly = False,
        required = False)

    pfbFile3 = TextLine(
        title = _("font3 pfb path"),
        description = _("Path to pfb file."),
        readonly = False,
        required = False)

    afmFile4 = TextLine(
        title = _("font4 afm path"),
        description = _("Path to afm file."),
        readonly = False,
        required = False)

    pfbFile4 = TextLine(
        title = _("font4 pfb path"),
        description = _("Path to pfb file."),
        readonly = False,
        required = False)

    afmFile5 = TextLine(
        title = _("font5 afm path"),
        description = _("Path to afm file."),
        readonly = False,
        required = False)

    pfbFile5 = TextLine(
        title = _("font5 pfb path"),
        description = _("Path to pfb file."),
        readonly = False,
        required = False)

    @invariant
    def logoFile1Exists(obj):
        """ does the file exists in local filesystem
        """
        if obj.logoFile1 is not None and \
           not os.access(obj.logoFile1, os.R_OK):
            raise Invalid(_(u"file '%s' in logo1 file path doesn't exists" % \
                            (obj.logoFile1)))
    @invariant
    def afmFile1Exists(obj):
        """ does the file exists in local filesystem
        """
        if obj.afmFile1 is not None and \
           not os.access(obj.afmFile1, os.R_OK):
            raise Invalid(_(u"file '%s' in font1 afm path doesn't exists" % \
                            (obj.afmFile1)))
    @invariant
    def afmFile2Exists(obj):
        """ does the file exists in local filesystem
        """
        if obj.afmFile2 is not None and \
           not os.access(obj.afmFile2, os.R_OK):
            raise Invalid(_(u"file '%s' in font2 afm path doesn't exists" % \
                            (obj.afmFile2)))
    @invariant
    def afmFile3Exists(obj):
        """ does the file exists in local filesystem
        """
        if obj.afmFile3 is not None and \
           not os.access(obj.afmFile3, os.R_OK):
            raise Invalid(_(u"file '%s' in font3 afm path doesn't exists" % \
                            (obj.afmFile3)))
    @invariant
    def afmFile4Exists(obj):
        """ does the file exists in local filesystem
        """
        if obj.afmFile4 is not None and \
           not os.access(obj.afmFile4, os.R_OK):
            raise Invalid(_(u"file '%s' in font4 afm path doesn't exists" % \
                            (obj.afmFile4)))
    @invariant
    def afmFile5Exists(obj):
        """ does the file exists in local filesystem
        """
        if obj.afmFile5 is not None and \
           not os.access(obj.afmFile5, os.R_OK):
            raise Invalid(_(u"file '%s' in font5 afm path doesn't exists" % \
                            (obj.afmFile5)))
    @invariant
    def pfbFile1Exists(obj):
        """ does the file exists in local filesystem
        """
        if obj.pfbFile1 is not None and \
           not os.access(obj.pfbFile1, os.R_OK):
            raise Invalid(_(u"file '%s' in font1 pfb path doesn't exists" % \
                            (obj.pfbFile1)))
    @invariant
    def pfbFile2Exists(obj):
        """ does the file exists in local filesystem
        """
        if obj.pfbFile2 is not None and \
           not os.access(obj.pfbFile2, os.R_OK):
            raise Invalid(_(u"file '%s' in font2 pfb path doesn't exists" % \
                            (obj.pfbFile2)))
    @invariant
    def pfbFile3Exists(obj):
        """ does the file exists in local filesystem
        """
        if obj.pfbFile3 is not None and \
           not os.access(obj.pfbFile3, os.R_OK):
            raise Invalid(_(u"file '%s' in font3 pfb path doesn't exists" % \
                            (obj.pfbFile3)))
    @invariant
    def pfbFile4Exists(obj):
        """ does the file exists in local filesystem
        """
        if obj.pfbFile4 is not None and \
           not os.access(obj.pfbFile4, os.R_OK):
            raise Invalid(_(u"file '%s' in font4 pfb path doesn't exists" % \
                            (obj.pfbFile4)))
    @invariant
    def pfbFile5Exists(obj):
        """ does the file exists in local filesystem
        """
        if obj.pfbFile5 is not None and \
           not os.access(obj.pfbFile5, os.R_OK):
            raise Invalid(_(u"file '%s' in font5 pfb path doesn't exists" % \
                            (obj.pfbFile5)))

    def generateAllPdf(absFilename):
        """
        will generate a complete pdf report
        """

class IRptPdf(Interface):
    """Interface of PDF-report-Adapter
    """
    def traverse4RptPre(level, comments):
        """pdf report object preamble
        
        level: indent-level (int 0..)
        comments: should there comments are in the output?

        """

    def traverse4RptPost(level, comments):
        """pdf report object postamble
        
        level: indent-level (int 0..)
        comments: should there comments are in the output?

        """

    def traverse4RptBody(level, comments):
        """pdf report data of/in object
        
        level: indent-level (int 0..)
        comments: should there comments are in the output?

        """

    def traverse4Rpt(level, comments):
        """object pdf report
        
        level: indent-level (int 0..)
        comments: should there comments are in the output?

        """
