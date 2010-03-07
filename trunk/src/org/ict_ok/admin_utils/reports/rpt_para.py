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
"""rpt_para 

Paragraph class for ict-ok.org reporting 
"""

__version__ = "$Id$"

# phython imports
import logging
from copy import deepcopy

# reportlab imports
from reportlab.platypus import ParaLines, Paragraph

# ict-ok.org imports
from org.ict_ok.admin_utils.reports.rpt_base import RptSuperclass
#from org.ict_ok.admin_utils.reports.rpt_style import rptNormalStyle

logger = logging.getLogger("AdmUtilReports")



class RptPara(RptSuperclass, Paragraph):
    """Paragraph class for ict-ok.org reporting
    """

    def __init__(self, text, style = None, bulletText = None, \
                 frags=None, caseSensitive=1, encoding='utf8', doc = None):
        """
        constructor of the object
        """
        RptSuperclass.__init__(self, doc)
        if style:
            style_d = style
        elif doc:
            style_d = doc.styles['Para']
        else:
            style_d = None
        try:
            Paragraph.__init__(self, text, style_d, bulletText, \
                               frags, caseSensitive, encoding)
        except ValueError, errText:
            logger.error(u'Error in RptPara: <%s>' % errText)
            logger.error(u'orig. Text: <%s>' % text)
        self._element_type = "paragraph"

    def __str__(self):
        return unicode(self.getText())

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

    def split(self, availWidth, availHeight):
        if len(self.frags) <= 0:
            return []
        #the split information is all inside self.blPara
        if not hasattr(self, 'blPara'):
            self.wrap(availWidth, availHeight)
        blPara = self.blPara
        style = self.style
        leading = style.leading
        lines = blPara.lines
        cnt = len(lines)
        space = int(availHeight / leading)
        if space <= 1:
            del self.blPara
            return []
        if cnt <= space:
            return [self]
        func = self._get_split_blParaFunc()
        # must overload - in orig method self.__class__ is referenced
        para1 = Paragraph(None, style, bulletText=self.bulletText,
                       frags=func(blPara, 0, space))
        #this is a major hack
        para1.blPara = ParaLines(kind=1, lines=blPara.lines[0:space],
                                 aH=availHeight, aW=availWidth)
        para1._JustifyLast = 1
        para1._splitpara = 1
        para1.height = space * leading
        para1.width = availWidth
        if style.firstLineIndent != 0:
            style = deepcopy(style)
            style.firstLineIndent = 0
        # must overload - in orig method self.__class__ is referenced
        para2 = Paragraph(None, style, bulletText=None,
                       frags=func(blPara, space, cnt))
        return [para1, para2]
