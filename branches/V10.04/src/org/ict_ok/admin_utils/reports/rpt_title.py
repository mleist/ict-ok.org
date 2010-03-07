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
from zope.configuration.xmlconfig import _context
"""rpt_title 

Title class for ict-ok.org reporting 
"""

__version__ = "$Id$"

# reportlab imports
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, PageBreak, KeepTogether, CondPageBreak,FrameBreak
from reportlab.platypus.tables import TableStyle, Table

# ict-ok.org imports
from org.ict_ok.admin_utils.reports.rpt_base import RptSuperclass

rpt_tbl_style = TableStyle([\
    ('LEFTPADDING', (0,0), (-1,-1), 0),
    ('RIGHTPADDING', (0,0), (-1,-1), 0),
    #('BOTTOMPADDING', (0,0), (-1,-1), 0),
    #('TOPPADDING', (0,0), (-1,-1), 0),
    ('ALIGN', (0,0), (0,-1), 'RIGHT'),
])        

class RptTitle(RptSuperclass, Paragraph):
    """Title class for IKOMtrol reporting
    """

    def __init__(self, text, intype='Heading1', doc=None, context=None):
        """
        constructor of the object
        """
        RptSuperclass.__init__(self, doc, context)
        self.setText(text)
        self._element_type = "title"
        self._type = intype
        
    def genElements(self):
        colWidths = [25 * mm, 5 * mm, None]
        if self._type.lower() == "heading1":
            numString = u'%(Chapter01+)s.'
        elif self._type.lower() == "heading2":
            numString = u'%(Chapter01)s.%(Chapter02+)s.'
        elif self._type.lower() == "heading3":
            numString = u'%(Chapter01)s.%(Chapter02)s.%(Chapter03+)s.'
        elif self._type.lower() == "heading4":
            numString = u'%(Chapter01)s.%(Chapter02)s.%(Chapter03)s.' \
                      u'%(Chapter04+)s.'
        elif self._type.lower() == "heading5":
            numString = u'%(Chapter01)s.%(Chapter02)s.%(Chapter03)s.' \
                      u'%(Chapter04)s.%(Chapter05+)s.'
        elif self._type.lower() == "heading6":
            numString = u'%(Chapter01)s.%(Chapter02)s.%(Chapter03)s.' \
                      u'%(Chapter04)s.%(Chapter05)s.%(Chapter02+)s.'
        elif self._type.lower() == "title":
            numString = u''
        else:
            numString = u'%(Chapter01)s.'
            
        p_1 = Paragraph(numString % self.getDocument().seq,
                        self.getDocument().styles[self._type+"r"])
        p_2 = Paragraph(self.getText(), \
                        self.getDocument().styles[self._type])
        t_1 = Table([[p_1, None , p_2]],
                    style=rpt_tbl_style,
                    colWidths=colWidths,
                    hAlign='LEFT')
        # for href stuff
        if hasattr(self._context, 'objectID'):
            t_1.ikoid = self._context.objectID
        if self.getDocument().firstH1Seen:
            t_1.keepWithNext = True
        t_1.ik_type = self._type
        if self._type.lower() == "heading1" or \
            self._type.lower() == "title":
            if self.getDocument().firstH1Seen:
                return KeepTogether([CondPageBreak(A4[1]/5), t_1])
            else:
                self.getDocument().firstH1Seen = True
                return t_1
        else:
            return t_1

    def __str__(self):
        return u"-- " + unicode(self.getText()) + u" --"

    def setText(self, arg_bodytext=u""):
        if len(self._content) > 0:
            self._content[0] = arg_bodytext
        else:
            self._content.append(arg_bodytext)

    def getText(self):
        if len(self._content) > 0:
            return self._content[0]
        else:
            return None
