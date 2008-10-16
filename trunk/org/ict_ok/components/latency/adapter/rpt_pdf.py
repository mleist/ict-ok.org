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
"""Adapter implementation for generating graphviz-dot configuration
"""


__version__ = "$Id$"

# python imports
from tempfile import _RandomNameSequence as RandomNameSequence
import time

# zope imports
from zope.interface import implements
from zope.component import adapts
from zope.i18nmessageid import MessageFactory

# reportlab imports
from reportlab.lib.units import mm, cm
from reportlab.platypus import Image, Spacer
from reportlab.platypus.tables import Table, TableStyle


# ict_ok.org imports
from org.ict_ok.components.latency.interfaces import ILatency
from org.ict_ok.components.supernode.adapter.rpt_pdf import \
     RptPdf as ParentRptPdf
from org.ict_ok.admin_utils.reports.interfaces import IRptPdf

_ = MessageFactory('org.ict_ok')


class RptPdf(ParentRptPdf):
    """adapter implementation of latency -> PDF Report
    """

    implements(IRptPdf)
    adapts(ILatency)

    def traverse4RptBody(self, level, comments):
        """pdf report data of/in object
        
        level: indent-level (int 0..)
        comments: should there comments are in the output?
        """
        if comments:
            self.writeComment(u"%s## Body (%s,%d) - LatencyRptPdfBody" % \
                              ("\t" * level, self.context.ikName, level))

    def traverse4RptPre(self, level, comments):
        """pdf report object preamble
        
        level: indent-level (int 0..)
        comments: should there comments are in the output?
        """
        ParentRptPdf.traverse4RptPre(self, level, comments)
        if comments:
            self.writeComment(u"%s## Pre2 (%s,%d) - LatencyRptPdfPre2" % \
                              ("\t" * level, self.context.ikName, level))
        if self.document:
            currtime = time.time()
            fileExt = RandomNameSequence().next()
            hours = 24
            params = {}
            params['imgtype'] = "PNG"
            params['nameext'] = "_%dh" % hours
            params['starttime'] = currtime - 3600 * hours
            params['endtime'] = currtime
            params['width'] = 900
            params['height'] = 266
            params['targetname'] = str("/tmp/%s%s_%s.png" % \
                                       (str(self.context.objectID),
                                        params['nameext'],
                                        fileExt))
            self.context.generateValuePng(params)
            im = Image(params['targetname'], width=13.5*cm, height=4*cm)
            im.hAlign = 'RIGHT'
            self.document.append(im)
            self.document.append(Spacer(0, 4 * mm))
            self.appendFile2Delete(params['targetname'])
