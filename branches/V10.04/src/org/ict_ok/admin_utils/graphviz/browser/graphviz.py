# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0232,W0142,R0901
#
"""implementation of browser class of the graphviz-utility 
"""

__version__ = "$Id$"

# python imports
from datetime import datetime

# zope imports
from zope.app import zapi
from zope.proxy import removeAllProxies
from zope.i18nmessageid import MessageFactory
from zope.app.rotterdam.xmlobject import setNoCacheHeaders
from zope.component import queryUtility

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.admin_utils.usermanagement.usermanagement import \
     getUserTimezone
from org.ict_ok.components.superclass.browser.superclass import \
     DisplayForm, EditForm
from org.ict_ok.admin_utils.graphviz.interfaces import IAdmUtilGraphviz
from org.ict_ok.admin_utils.graphviz.graphviz import \
     AdmUtilGraphviz
from org.ict_ok.version import getIkVersion

_ = MessageFactory('org.ict_ok')


# --------------- helper functions -------------------------

# --------------- menu entries -----------------------------

class MSubGraphvizAll(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'All Graphs')
    viewURL = '@@graphvizAll.html'
    weight = 999

# --------------- object details ---------------------------
class AdmUtilGraphvizDetails(SupernodeDetails):
    """Browser implementation of Graphviz picture generator
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + ['ikName']
    omit_editfields = SupernodeDetails.omit_editfields + ['ikName']

    def getPngFile(self):
        """get dot file and convert to png
        """
        utilGraphviz = queryUtility(IAdmUtilGraphviz, name='AdmUtilGraphviz')
        my_formatter = self.request.locale.dates.getFormatter(
            'dateTime', 'medium')
        userTZ = getUserTimezone()
        longTimeString = my_formatter.format(\
            userTZ.fromutc(datetime.utcnow()))
        versionStr = "%s [%s]" % (longTimeString, getIkVersion())
        self.request.response.setHeader('Content-Type', 'image/png')
        filename = "graphviz_%s.png" % self.context.ikName
        self.request.response.setHeader(\
            'Content-Disposition',
            'attachment; filename=\"%s\"' % filename)
        setNoCacheHeaders(self.request.response)
        return utilGraphviz.getPngFile(self.context, self.request)

    def getCmapxText(self):
        """get dot file and convert to client side image map
        """
        utilGraphviz = queryUtility(IAdmUtilGraphviz, name='AdmUtilGraphviz')
        my_formatter = self.request.locale.dates.getFormatter(
            'dateTime', 'medium')
        userTZ = getUserTimezone()
        longTimeString = my_formatter.format(\
            userTZ.fromutc(datetime.utcnow()))
        versionStr = "%s [%s]" % (longTimeString, getIkVersion())
        setNoCacheHeaders(self.request.response)
        return utilGraphviz.getCmapxText(self.context, self.request)


    def getValuePngHref(self):
        """get path of object as string
        """
        obj = removeAllProxies(self.context)
        return zapi.absoluteURL(obj, self.request)

    #def graphvizAll(self):
        #"""
        #will send the complete dot report to the browser
        #"""
        #utilGraphviz = queryUtility(IAdmUtilGraphviz, name='AdmUtilGraphviz')
        #my_formatter = self.request.locale.dates.getFormatter(
            #'dateTime', 'medium')
        #userTZ = getUserTimezone()
        #longTimeString = my_formatter.format(\
            #userTZ.fromutc(datetime.utcnow()))
        #versionStr = "%s [%s]" % (longTimeString, getIkVersion())
        ##self.request.response.setHeader('Content-Type', 'image/png')
        ##filename = "*.png"
        ##self.request.response.setHeader(\
            ##'Content-Disposition',
            ##'attachment; filename=\"%s\"' % filename)
        #setNoCacheHeaders(self.request.response)
        #return utilGraphviz.getCmapxText(self.context, self.request)


class AdmUtilGraphvizAll(AdmUtilGraphvizDetails):
    pass
# --------------- forms ------------------------------------


class ViewAdmUtilGraphvizForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of graphviz adapter')
    factory = AdmUtilGraphviz
    omitFields = AdmUtilGraphvizDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class EditAdmUtilGraphvizForm(EditForm):
    """ Edit for for net """
    label = _(u'edit graphviz adapter')
    factory = AdmUtilGraphviz
    omitFields = AdmUtilGraphvizDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)
