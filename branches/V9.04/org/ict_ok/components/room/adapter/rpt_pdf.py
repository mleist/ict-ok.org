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
from org.ict_ok.components.room.interfaces import IRoom
from org.ict_ok.components.room.room import Room
from org.ict_ok.components.room.browser.room import \
         RoomDetails
from org.ict_ok.components.supernode.adapter.rpt_pdf import \
     RptPdf as ParentRptPdf
from org.ict_ok.admin_utils.reports.interfaces import IRptPdf


# ict_ok.org imports
class RptPdf(ParentRptPdf):
    """adapter implementation of Room -> PDF Report
    """

    implements(IRptPdf)
    adapts(IRoom)
    factory = Room
    omitFields = RoomDetails.omit_viewfields

    def getRefTitle(self):
        import pdb
        pdb.set_trace()
        retString = u"<a href='%s' color='blue'>%s</a>" % \
                    (self.context.objectID, self.context.ikName)
        if self.context.building is not None:
            if self.document and \
                self.document._reporter and \
                self.context.building in \
                    self.document._reporter.allContentObjects:
                retString += u" / <a href='%s' color='blue'>%s</a>" % \
                        (self.context.building.objectID,
                         self.context.building.ikName)
            else:
                retString += u" / %s" % \
                        (self.context.building.ikName)
            if self.context.building.location is not None:
                if self.document and \
                    self.document._reporter and \
                    self.context.building.location in \
                        self.document._reporter.allContentObjects:
                    retString += u" / <a href='%s' color='blue'>%s</a>" % \
                            (self.context.building.location.objectID,
                             self.context.building.location.ikName)
                else:
                    retString += u" / %s" % \
                            (self.context.building.location.ikName)
        return retString
