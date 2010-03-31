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
"""rpt_document

Document class for ict-ok.org reporting 
"""

__version__ = "$Id$"

# reportlab imports
from reportlab.platypus import BaseDocTemplate
from reportlab.lib.units import mm, cm
from reportlab.lib.pagesizes import A4, A3
from reportlab.lib.sequencer import Sequencer

# ict-ok.org imports
from org.ict_ok.admin_utils.reports.rpt_base import RptSuperclass
from org.ict_ok.admin_utils.reports.rpt_page import RptPageTemplate
from org.ict_ok.admin_utils.reports.rpt_frame import RptFrame
from org.ict_ok.admin_utils.reports.rpt_font import \
     addMappingRptFonts, registerRptFonts
from org.ict_ok.admin_utils.reports.rpt_style import getRptStyleSheet

class RptDocument(RptSuperclass, BaseDocTemplate):
    """document class for ict-ok.org reporting
    """
    def __init__(self, filename="/tmp/rpt001.pdf", **kw):
        """
        constructor of the object
        """
        RptSuperclass.__init__(self)
        self._element_type = "document"
        BaseDocTemplate.__init__(self, filename, **kw)
        self.pagesize = A4
        self.title = u"ict-ok.org Report"
        self.author = u"ict-ok.org"
        self.subject = u"ict-ok.org Report"
        self.leftMargin = 2*cm
        self.rightMargin = 2*cm
        self.topMargin = 2*cm
        self.bottomMargin = 2*cm
        self.showBoundary = False
        #self.allowSplitting = False
        rptFrame01 = RptFrame(2*cm, 25*mm, 165*mm, 24.7*cm) # , showBoundary=True)
        rptPageT01 = RptPageTemplate(u"RptTP1", [rptFrame01], pagesize=A4)
        self.addPageTemplates(rptPageT01)
        registerRptFonts()
        #addMappingRptFonts()
        self.styles = getRptStyleSheet()
        self.seq = Sequencer()
        self.seq.chain('Chapter01', 'Chapter02')
        self.seq.chain('Chapter02', 'Chapter03')
        self.seq.chain('Chapter03', 'Chapter04')
        self.seq.chain('Chapter04', 'Chapter05')
        self.seq.chain('Chapter05', 'Chapter06')
        self.volumeNo = None
        self.authorName = None
        self.versionStr = None
        self.firstPageTitle = None
        self.lastPageTitle = None
        self.firstH1Seen = False
        
    def __str__(self):
        return u""

    def setVolumeNo(self, arg_VolumeNo = None):
        self.volumeNo = arg_VolumeNo

    def setAuthorName(self, arg_AuthorName = None):
        self.authorName = arg_AuthorName

    def setVersionStr(self, arg_VersionStr = None):
        self.versionStr = arg_VersionStr

    def buildPdf(self):
#        self.build(self._content)
        from reportlab.platypus.doctemplate import LayoutError
        self.multiBuild(self._content)
#        try:
#            self.multiBuild(self._content)
#        except AttributeError, errText:
#            print errText
#            raise AttributeError(errText)
#        except LayoutError, errText:
#            print errText
#            raise LayoutError(errText)

    def afterFlowable(self, flowable):
        if flowable.__class__.__name__ == 'Table':
            try:
                styleName = flowable.ik_type
            except AttributeError:
                styleName = ""
            if styleName[:5] == 'Title':
                text = flowable._cellvalues[0][2].getPlainText()
                nbr = flowable._cellvalues[0][0].getPlainText()
                self.lastPageTitle = "%s %s" % (nbr, text)
                if not self.firstPageTitle:
                    self.firstPageTitle = "%s %s" % (nbr, text)
            if styleName[:7] == 'Heading':
                text = flowable._cellvalues[0][2].getPlainText()
                level = int(styleName[7:])
                pageNum = self.page
                if styleName[:8] == 'Heading1':
                    self.notify('TOCEntry', (level, text, pageNum))
                key = str(hash(flowable))
                c = self.canv
                c.bookmarkPage(key)
                if hasattr(flowable, 'ikoid'):
                    c.bookmarkPage(str(flowable.ikoid))
                c.addOutlineEntry(text, key, level=level-1, closed=0)
                nbr = flowable._cellvalues[0][0].getPlainText()
                self.lastPageTitle = "%s %s" % (nbr, text)
                if not self.firstPageTitle:
                    self.firstPageTitle = "%s %s" % (nbr, text)
        if flowable.__class__.__name__ == 'Paragraph':
            styleName = flowable.style.name
            if styleName[:5] == 'Title':
                text = flowable.getPlainText()
                self.lastPageTitle = "%s %s" % (nbr, text)
                if not self.firstPageTitle:
                    self.firstPageTitle = "%s %s" % (nbr, text)
            if styleName[:7] == 'Heading':
                text = flowable.getPlainText()
                level = int(styleName[7:])
                pageNum = self.page
                if styleName[:8] == 'Heading1':
                    self.notify('TOCEntry', (level, text, pageNum))
                key = str(hash(flowable))
                c = self.canv
                c.bookmarkPage(key)
                if hasattr(flowable, 'ikoid'):
                    c.bookmarkPage(str(flowable.ikoid))
                c.addOutlineEntry(text, key, level=level-1, closed=0)
                nbr = flowable._cellvalues[0][0].getPlainText()
                self.lastPageTitle = "%s %s" % (nbr, text)
                if not self.firstPageTitle:
                    self.firstPageTitle = "%s %s" % (nbr, text)


    def myFirstPage(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Meta2Korrespondenz-Roman', 16)
        canvas.drawCentredString(self.pagesize[0]/2.0, self.pagesize[1]-108, Title)
        canvas.setFont('Meta2Korrespondenz-Roman',9)
        canvas.drawString(1.0 * cm, 1.0 * cm, "First Page / %s" % pageinfo)
        canvas.restoreState()

    def myLaterPages(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Meta2Korrespondenz-Roman', 9)
        canvas.drawString(1.0 * cm, 1.0 * cm, "Page %d %s" % (doc.page, pageinfo))
        canvas.restoreState()
