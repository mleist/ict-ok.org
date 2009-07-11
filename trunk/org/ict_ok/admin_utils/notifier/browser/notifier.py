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
"""implementation of browser class of Object-Message-Queue-Utility
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.app import zapi
from zope.i18nmessageid import MessageFactory
from zope.app.intid.interfaces import IIntIds
from zope.component import getUtility
from zope.security import checkPermission
from zope.app.pagetemplate.urlquote import URLQuote

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     DisplayForm, EditForm, Overview
from org.ict_ok.admin_utils.notifier.notifier import NotifierUtil
from org.ict_ok.components.interfaces import IComponent

_ = MessageFactory('org.ict_ok')


class NotifierDetails(SupernodeDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + ['ikName', 'notifierSet']
    omit_editfields = SupernodeDetails.omit_editfields + ['ikName']

    def actions(self):
        """
        gives us the action dict of the object
        """
        try:
            objId = getUtility(IIntIds).getId(self.context)
        except KeyError:
            objId = 1000
        retList = []
        if checkPermission('org.ict_ok.admin_utils.notifier.Send',
                           self.context):
            quoter = URLQuote(self.request.getURL())
            tmpDict = {}
            tmpDict['oid'] = u"c%snotifier_send" % objId
            tmpDict['title'] = _(u"send test")
            tmpDict['href'] = u"%s/@@send_test?nextURL=%s" % \
                   (zapi.absoluteURL(self.context, self.request),
                    quoter.quote())
            tmpDict['tooltip'] = _(u"will send a test message "\
                                   u"by the selected notifier")
            retList.append(tmpDict)
        return retList

    def send_test(self):
        """
        will send a test message by the notifier
        """
        testMsg = """This is a test message from
        """
        self.context.send_test(testMsg)
        nextURL = self.request.get('nextURL', default=None)
        if nextURL:
            return self.request.response.redirect(nextURL)
        else:
            return self.request.response.redirect('./@@details.html')

    def getAllNotifierObjs(self):
        """
        get list of Notifier-Tupel (name, obj)
        """
        retList = []
        for name, notifier in self.context.getAllNotifierObjs():
            retDict = {}
            retDict['name'] = name
            retDict['href'] = zapi.absoluteURL(notifier, self.request) + '/@@details.html'
            retList.append(retDict)
        return retList
        
    def getNotifierObjs(self):
        """
        get list of Notifier-Tupel (name, obj)
        """
        retList = []
        if self.context.getNotifierObjs() is not None:
            for name, notifier in self.context.getNotifierObjs():
                retDict = {}
                retDict['name'] = name
                retDict['href'] = zapi.absoluteURL(notifier, self.request) + '/@@details.html'
                retList.append(retDict)
        return retList


# --------------- forms ------------------------------------


class ViewNotifierForm(DisplayForm):
    """ Display form for the notifier """
    label = _(u'settings of notifier')
    factory = NotifierUtil
    omitFields = NotifierDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class EditNotifierForm(EditForm):
    """ Edit for for notifier """
    label = _(u'edit notifier')
    factory = NotifierUtil
    omitFields = NotifierDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)


class ViewNotifications(Overview):
    label = _(u"Notifications")
    #def update(self):
        #self.label = _(u"Dashboard of %s") % \
            #self.request.principal.title
        #Overview.update(self)
    def objs(self):
        """List of Content objects"""
        retList = []
        uidutil = getUtility(IIntIds)
        for (myid, myobj) in uidutil.items():
            if IComponent.providedBy(myobj.object):
                tmp_health = myobj.object.get_health()
                if tmp_health is not None and \
                   tmp_health < 0.9:
                    retList.append(myobj.object)
        return retList
    #def objs(self):
        #"""List of Content objects"""
        #retList = []
        #userProps = AdmUtilUserProperties(self.request.principal)
        #for dashboardItem in userProps.dashboard_objs:
            #myObj = dashboardItem.getObject(some_obj=self,
                                            #arg_request=self.request)
            #if myObj is not None:
                #retList.append(myObj)
        #return retList
    #if IComponent.providedBy(item):
        #try:
            #return u"%3.0f %%" % (100.0 * item.get_health())
        #except TypeError:
            #return u"-"
