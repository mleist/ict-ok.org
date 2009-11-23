# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
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

# python imports

# zope imports
from zope.app import zapi
from zope.i18nmessageid import MessageFactory

# zc imports
from zc.table.column import GetterColumn
from zc.table.table import StandaloneFullFormatter

# z3c imports
from z3c.pagelet.browser import BrowserPagelet

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory
from org.ict_ok.admin_utils.eventcrossbar.eventcrossbar import \
     AdmUtilEventCrossbar
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


class MSubCrossBarSignalGraph(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Signal Graph')
    viewURL = 'signalgraph.html'
    weight = 30


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
        return self.context.getEventCrossbarTime()

    def getIMGFile(self):
        """get dot file and convert to png
        """
        imgtype = self.request.get('type', default='png')
        mode = self.request.get('mode', default=None)
        if mode and mode.lower() == "fview":
            self.request.response.setHeader('content-type',
                                            'image/%s' % imgtype)
            self.request.response.setHeader('content-disposition',
                                            'attachment; filename=\"signals.%s\"'\
                                            % (imgtype))
        return self.context.getIMGFile(imgtype, mode)

    #def getCmapxText(self):
        #"""get dot file and convert to client side image map
        #"""
        #return self.context.getCmapxText(zapi.getRoot(self))



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


class SignalGraph(BrowserPagelet):
    label = _(u'Signal Overview')

    def getValuePngHref(self):
        """get path of object as string
        """
        return zapi.absoluteURL(self.context, self.request)


# --------------- forms ------------------------------------


class DetailsAdmUtilEventCrossbarForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Event')
    factory = AdmUtilEventCrossbar
    omitFields = AdmUtilEventCrossbarDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class EditAdmUtilEventCrossbarForm(EditForm):
    """ Edit form for the object """
    label = _(u'edit crossbar properties')
    factory = AdmUtilEventCrossbar
    omitFields = AdmUtilEventCrossbarDetails.omit_editfields

    fields = fieldsForFactory(factory, omitFields)
