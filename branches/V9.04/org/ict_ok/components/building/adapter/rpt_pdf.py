# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0142
#
"""Adapter implementation for generating pdf reports of HardwareAppliance"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.component import adapts

# ict_ok.org imports
from org.ict_ok.components.building.interfaces import IBuilding
from org.ict_ok.components.building.building import Building
from org.ict_ok.components.building.browser.building import BuildingDetails
from org.ict_ok.components.supernode.adapter.rpt_pdf import \
     RptPdf as ParentRptPdf
from org.ict_ok.admin_utils.reports.interfaces import IRptPdf


class RptPdf(ParentRptPdf):
    """adapter implementation of Building -> PDF Report
    """

    implements(IRptPdf)
    adapts(IBuilding)
    factory = Building
    omitFields = BuildingDetails.omit_viewfields

    def getRefTitle(self):
        retString = u"<a href='%s' color='blue'>%s</a>" % \
                    (self.context.objectID, self.context.ikName)
        if self.context.location is not None:
            if self.document and \
                self.document._reporter and \
                self.context.location in \
                    self.document._reporter.allContentObjects:
                retString += u" / <a href='%s' color='blue'>%s</a>" % \
                        (self.context.location.objectID,
                         self.context.location.ikName)
            else:
                retString += u" / %s" % \
                        (self.context.location.ikName)
        return retString
