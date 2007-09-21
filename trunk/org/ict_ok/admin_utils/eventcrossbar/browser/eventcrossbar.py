# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0232,W0142
#
"""implementation of browser class of eventCrossbar handler
"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.i18nmessageid import MessageFactory
from zope.dublincore.interfaces import IZopeDublinCore

# zc imports
from zc.table.column import GetterColumn
from zc.table.table import StandaloneFullFormatter

# z3c imports
from z3c.form import field
from z3c.pagelet.browser import BrowserPagelet

# ict_ok.org imports
from org.ict_ok.admin_utils.eventcrossbar.interfaces import \
     IAdmUtilEventCrossbar
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DisplayForm, EditForm
from org.ict_ok.skin.menu import GlobalMenuSubItem

_ = MessageFactory('org.ict_ok')

# --------------- menu entries -----------------------------


class MSubCrossBar(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Crossbar')
    viewURL = 'crossbar.html'
    weight = 20



class AdmUtilEventCrossbarDetails(SupernodeDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + ['ikName']
    omit_editfields = SupernodeDetails.omit_editfields + ['ikName']

    def getInstanceCounter(self):
        """convert instance counter for display
        """
        return self.context.getInstanceCounter()

    def getEventCrossbarTime(self):
        """convert eventcrossbar timestamp for display
        """
        from zope.proxy import removeAllProxies
        from zope.traversing.browser import absoluteurl
        obj = removeAllProxies(self.context)
        print "#########->", absoluteurl.absoluteURL(obj, self.request)
        return self.context.getEventCrossbarTime()


class CrossBar(BrowserPagelet):
    label = _(u'event crossbar')
    mytest = [u'a', u'b', u'c', u'd', u'e', u'f', u'g']
    def update(self):
        self.columns = (\
            GetterColumn(title="1111",
                         ),
            GetterColumn(title="2222",
                         ),
            GetterColumn(title="3333",
                         ),
        )
    def objs(self):
        """List of Content objects"""
        retList = []
        try:
            for obj in self.mytest:
                retList.append(obj)
        except:
            pass
        #try:
            #for obj in self.context.values():
                #if ISuperclass.providedBy(obj):
                    #retList.append(obj)
        #except:
            #pass
        return retList

    def table(self):
        """ Properties of table are defined here"""
        formatter = StandaloneFullFormatter(
            self.context, self.request, self.objs(),
            columns=self.columns)
        formatter.cssClasses['table'] = 'listing'
        return formatter()

# --------------- forms ------------------------------------


class DetailsAdmUtilEventCrossbarForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Event')
    fields = field.Fields(IAdmUtilEventCrossbar).omit(\
        *AdmUtilEventCrossbarDetails.omit_viewfields) + \
           field.Fields(IZopeDublinCore).select('modified')


class EditAdmUtilEventCrossbarForm(EditForm):
    """ Edit form for the object """
    label = _(u'edit crossbar properties')
    fields = field.Fields(IAdmUtilEventCrossbar).omit(\
        *AdmUtilEventCrossbarDetails.omit_editfields)
